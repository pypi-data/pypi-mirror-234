
from typing import Dict, Optional,Callable
import os,torch
from transformers.modeling_utils import unwrap_model,PreTrainedModel
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers.trainer import TRAINING_ARGS_NAME, WEIGHTS_NAME
from ailab.utils.other import get_state_dict,load_valuehead_params,plot_loss,VALUE_HEAD_FILE_NAME
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
from trl import PreTrainedModelWrapper

class PeftTrainer(Seq2SeqTrainer):
    r"""
    Inherits Seq2SeqTrainer to support parameter-efficient checkpoints.
    """

    def __init__(self, finetune_type, **kwargs):
        self.finetune_type = finetune_type
        super().__init__(**kwargs)

    def _save(self, output_dir: Optional[str] = None, state_dict: Optional[Dict[str, torch.Tensor]] = None) -> None:
        r"""
        Saves trainable parameters as model checkpoint.

        This function will only be executed at the process zero.

        Subclass and override to inject custom behavior. It should not be directly used by external scripts.
        """
        output_dir = output_dir if output_dir is not None else self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}")
        model = unwrap_model(self.model)

        if isinstance(model, PreTrainedModelWrapper):
            # Custom state dict: https://github.com/lvwerra/trl/blob/v0.4.7/trl/models/modeling_value_head.py#L200
            model_state_dict = state_dict or model.state_dict()
            v_head_state_dict = {
                name.replace("v_head.", ""): model_state_dict[name].cpu().clone().detach()
                for name in model_state_dict.keys() if name.startswith("v_head.")
            }

            torch.save(v_head_state_dict, os.path.join(output_dir, VALUE_HEAD_FILE_NAME))
            model = model.pretrained_model

        state_dict = state_dict or get_state_dict(model)
        from peft import PeftModel
        if isinstance(model, (PeftModel, PreTrainedModel)):
            model.config.use_cache = True
            model.save_pretrained(output_dir, state_dict=state_dict, safe_serialization=self.args.save_safetensors)
            model.config.use_cache = False
        else:
            torch.save(state_dict, os.path.join(output_dir, WEIGHTS_NAME))

        if self.finetune_type == "full" and self.tokenizer is not None:
            try:
                self.tokenizer.save_pretrained(output_dir)
            except:
                logger.warning("Cannot save tokenizer, copy the files manually.")

        with open(os.path.join(output_dir, TRAINING_ARGS_NAME), "w", encoding="utf-8") as f:
            f.write(self.args.to_json_string() + "\n")

    def _load_best_model(self):
        r"""
        Loads trainable parameters from model checkpoint.

        Subclass and override to inject custom behavior. It should not be directly used by external scripts.
        """
        logger.info(f"Loading best model from {self.state.best_model_checkpoint} (score: {self.state.best_metric}).")

        model = unwrap_model(self.model)
        backbone_model = getattr(model, "pretrained_model") if hasattr(model, "pretrained_model") else model
        backbone_model.load_adapter(self.state.best_model_checkpoint, getattr(backbone_model, "active_adapter"))
        if hasattr(model, "v_head") and load_valuehead_params(model, self.state.best_model_checkpoint):
            model.v_head.load_state_dict({
                "summary.weight": getattr(model, "reward_head_weight"),
                "summary.bias": getattr(model, "reward_head_bias")
            })

@TrainerRg.register((Task.question_answering, Model.chatglm_6b))
@TrainerRg.register((Task.question_answering, Model.chatglm2_6b))
@TrainerRg.register((Task.question_answering, Model.code_geex_2))
@TrainerRg.register((Task.question_answering, Model.finGPT_chatglm2_v3))
class ChatglmTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        finetune_type = kwargs['model_args'].get('finetune_type', 'lora')
        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_no_offload.json")
        train_args['ddp_find_unused_parameters'] = False
        train_args['ddp_timeout'] = 30000
        train_args['deepspeed'] = deepspeed_dir

        from ailab.utils.parse_args import get_train_args
        _, training_args = get_train_args(train_args)
        
        logger.info(f'training_args {training_args}')
        
        stage = kwargs['model_args'].get('stage', 'sft')
        if stage == 'sft':
            trainer = PeftTrainer(
                finetune_type=finetune_type,
                model=model.model_ins,
                train_dataset=dataset.to_hf_dataset()['train'],
                eval_dataset=dataset.to_hf_dataset()['test'],
                args=training_args,
                tokenizer=preprocessor.preprocessor_ins,
                data_collator=data_collator.datacollator_ins,
                callbacks=[TrainProgress(train_progress)],
            )
        elif stage == 'dpo':
            from trl import DPOTrainer
            training_args.remove_unused_columns = False
            trainer = DPOTrainer(
                model=model.model_ins,
                train_dataset=dataset.to_hf_dataset(),
                args=training_args,
                tokenizer=preprocessor.preprocessor_ins,
                max_length=512,
                max_prompt_length=128,
                callbacks=[TrainProgress(train_progress)],
            )

        self.trainer = trainer
        self.train_args = train_args
    
    def train(self):
        trainer = self.trainer
        output_dir = self.train_args.get('output_dir', 'my_model')
        resume_from_checkpoint = self.train_args.get('resume_from_checkpoint', False)
        end_to_zip = self.train_args.get('end_to_zip', False)

        if resume_from_checkpoint:
            from transformers.trainer_utils import get_last_checkpoint
            resume_from_checkpoint = get_last_checkpoint(output_dir)

        train_result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        trainer.log_metrics("train", train_result.metrics)
        trainer.save_metrics("train", train_result.metrics)
        trainer.save_state()
        trainer.save_model()

        if trainer.is_world_process_zero():
            plot_loss(output_dir, keys=["loss", "eval_loss"])
            if end_to_zip:
                from ailab.utils.other import create_zip_and_delete_folder
                zip_file_path = output_dir+"/adapter.zip"
                create_zip_and_delete_folder(output_dir,zip_file_path)
                
    def postprocess(self):
        metrics = self.trainer.evaluate()
        self.trainer.log_metrics("eval", metrics)
        self.trainer.save_metrics("eval", metrics)



