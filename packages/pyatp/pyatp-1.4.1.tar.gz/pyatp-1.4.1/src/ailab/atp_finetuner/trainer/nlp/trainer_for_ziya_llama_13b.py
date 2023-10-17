import os
from os.path import join
import math
from typing import Callable, Dict, List, Optional, Tuple, Union, Any
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import bitsandbytes as bnb
import torch
from torch.utils.data import Dataset
from torch import nn
import transformers
from transformers import (
    PreTrainedModel,
    TrainingArguments,
    DataCollator,
    PreTrainedTokenizerBase,
    EvalPrediction,
    TrainerCallback,
    set_seed,
)
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.utils.callbacks import TrainProgress
from ailab.log import logger

# Name of the files used for checkpointing
TRAINING_ARGS_NAME = "training_args.bin"
TRAINER_STATE_NAME = "trainer_state.json"
OPTIMIZER_NAME = "optimizer.pt"
SCHEDULER_NAME = "scheduler.pt"
SCALER_NAME = "scaler.pt"


@TrainerRg.register((Task.question_answering, Model.ziya_llama_13b))
class Ziyallama13bTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def find_all_linear_names(self,model):
        """
        找出所有全连接层，为所有全连接添加adapter
        """
        cls = bnb.nn.Linear4bit
        lora_module_names = set()
        for name, module in model.named_modules():
            if isinstance(module, cls):
                names = name.split(".")
                lora_module_names.add(names[0] if len(names) == 1 else names[-1])

        if "lm_head" in lora_module_names:  # needed for 16-bit
            lora_module_names.remove("lm_head")
        return list(lora_module_names)

    def preprocess(
        self,
        dataset: AILabDataset,
        model: AILabModel,
        preprocessor: AILabPreprocessor,
        data_collator: AILabDataCollator,
        metric: AILabMetric,
        train_progress: Callable,
        **kwargs,
    ):
        train_args = kwargs["train_args"]

        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir, "ds_zero2_no_offload.json")
        train_args['ddp_find_unused_parameters'] = False
        train_args['ddp_timeout'] = 30000
        train_args['deepspeed'] = deepspeed_dir

        from ailab.utils.parse_args import get_train_args
        _, training_args = get_train_args(train_args)
        logger.info(f'training_args {training_args}')
        if not os.path.exists(training_args.output_dir):
            os.makedirs(training_args.output_dir)

        # 根据model_name 生产model
        model = model.model_ins  # 根据model_name 生产model
        model = prepare_model_for_kbit_training(
            model, use_gradient_checkpointing=training_args.gradient_checkpointing
        )

        # 找到所有需要插入adapter的全连接层
        target_modules = self.find_all_linear_names(model)
        # 初始化lora配置
        lora_rank = 16
        lora_alpha = 32
        lora_dropout = 0.05
        config = LoraConfig(
            r=lora_rank,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, config)
        model.config.torch_dtype = torch.float32

        tokenizer = preprocessor.preprocessor_ins
        data_collator = data_collator.datacollator_ins

        trainer = LoRATrainer(
            model=model,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            tokenizer=tokenizer,
            data_collator=data_collator,
            callbacks=[TrainProgress(train_progress)],

        )
        self.trainer = trainer
        self.train_args = train_args

    def train(self):
        trainer = self.trainer
        output_dir = self.train_args.get('output_dir', 'my_model')
        resume_from_checkpoint = self.train_args.get('resume_from_checkpoint', False)
        end_to_zip = self.train_args.get('end_to_zip', False)

        # 保存最好的checkpoint
        train_result = trainer.train()
        final_save_path = join(output_dir, 'final')
        trainer.save_model(final_save_path)  # Saves the tokenizer too

        metrics = train_result.metrics
        metrics["train_samples"] = len(trainer.train_dataset)
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        trainer.save_state()

        logger.info("*** Evaluate ***")
        metrics = trainer.evaluate()
        metrics["eval_samples"] =len(trainer.eval_dataset)
        try:
            perplexity = math.exp(metrics["eval_loss"])
        except OverflowError:
            perplexity = float("inf")
        metrics["perplexity"] = perplexity

        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

        if trainer.is_world_process_zero() and end_to_zip:
            from ailab.utils.other import create_zip_and_delete_folder
            zip_file_path = output_dir+"/adapter.zip"
            create_zip_and_delete_folder(output_dir,zip_file_path)

    def postprocess(self):
        metrics = self.trainer.evaluate()
        self.trainer.log_metrics("eval", metrics)
        self.trainer.save_metrics("eval", metrics)

class LoRATrainer(transformers.Trainer):

    def __init__(
        self,
        model: Union[PreTrainedModel, nn.Module] = None,
        args: TrainingArguments = None,
        data_collator: Optional[DataCollator] = None,
        train_dataset: Optional[Dataset] = None,
        eval_dataset: Optional[Dataset] = None,
        tokenizer: Optional[PreTrainedTokenizerBase] = None,
        model_init: Callable[[], PreTrainedModel] = None,
        compute_metrics: Optional[Callable[[EvalPrediction], Dict]] = None,
        callbacks: Optional[List[TrainerCallback]] = None,
        optimizers: Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LambdaLR] = (
            None,
            None,
        ),
        preprocess_logits_for_metrics: Callable[
            [torch.Tensor, torch.Tensor], torch.Tensor
        ] = None,
    ):
        super(LoRATrainer, self).__init__(
            model=model,
            args=args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            model_init=model_init,
            compute_metrics=compute_metrics,
            callbacks=callbacks,
            optimizers=optimizers,
            preprocess_logits_for_metrics=preprocess_logits_for_metrics,
        )

    """
    修改checkkpoint的保存逻辑，只保存lora
    """
    def _save(self, output_dir: Optional[str] = None, state_dict=None):
        # If we are executing this function, we are the process zero, so we don't check for that.
        output_dir = output_dir if output_dir is not None else self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}")
        # 保存lora权重和配置
        self.model.save_pretrained(
            output_dir,
            state_dict=state_dict,
            safe_serialization=self.args.save_safetensors,
        )

        if self.tokenizer is not None:
            self.tokenizer.save_pretrained(output_dir)

        # Good practice: save your training arguments together with the trained model
        torch.save(self.args, os.path.join(output_dir, TRAINING_ARGS_NAME))
