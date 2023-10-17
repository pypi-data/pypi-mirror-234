import os
from typing import Callable
import torch
from transformers import TrainingArguments, Trainer
from peft import get_peft_model_state_dict, set_peft_model_state_dict
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

@TrainerRg.register((Task.question_answering, Model.vicuna))
@TrainerRg.register((Task.question_answering, Model.open_llama))
class Vicunatrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        
        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_no_offload.json")
        train_args['ddp_find_unused_parameters'] = False
        train_args['ddp_timeout'] = 30000
        train_args['deepspeed'] = deepspeed_dir

        from ailab.utils.parse_args import get_train_args
        _, training_args = get_train_args(train_args)

        logger.info(f'training_args {training_args}')

        trainer = Trainer(
            model=model.model_ins,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            data_collator=data_collator.datacollator_ins,
            callbacks=[TrainProgress(train_progress)],
        )
        self.trainer = trainer
        self.train_args = train_args

    def train(self):
        model = self.trainer.model
        resume_from_checkpoint = self.train_args.get('resume_from_checkpoint', False)
        end_to_zip = self.train_args.get('end_to_zip', False)
        output_dir = self.train_args.get('output_dir', 'my_model')

        from transformers.trainer_utils import get_last_checkpoint
        if resume_from_checkpoint:
            resume_from_checkpoint = get_last_checkpoint(output_dir)
            if resume_from_checkpoint is None:
                resume_from_checkpoint = False
            else:
                checkpoint_name = os.path.join(resume_from_checkpoint, "pytorch_model.bin")
                if not os.path.exists(checkpoint_name):
                    checkpoint_name = os.path.join(resume_from_checkpoint, "adapter_model.bin")
                if os.path.exists(checkpoint_name):
                    logger.info(f"Restarting from {checkpoint_name}")
                    adapters_weights = torch.load(checkpoint_name)
                    set_peft_model_state_dict(model, adapters_weights)
                else:
                    resume_from_checkpoint = False

        model.config.use_cache = False
        old_state_dict = model.state_dict
        model.state_dict = (
            lambda self, *_, **__: get_peft_model_state_dict(
                self, old_state_dict()
            )
        ).__get__(model, type(model))
        model = torch.compile(model)

        self.trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        model.save_pretrained(output_dir)

        if self.trainer.is_world_process_zero() and end_to_zip:
            from ailab.utils.other import create_zip_and_delete_folder
            zip_file_path = output_dir+"/adapter.zip"
            create_zip_and_delete_folder(output_dir,zip_file_path)

    def postprocess(self):
        metrics = self.trainer.evaluate()
        self.trainer.log_metrics("eval", metrics)
        self.trainer.save_metrics("eval", metrics)



