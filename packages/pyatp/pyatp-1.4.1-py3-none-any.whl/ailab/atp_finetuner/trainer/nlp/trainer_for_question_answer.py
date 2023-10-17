from typing import Callable
from transformers import TrainingArguments, Trainer
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

@TrainerRg.register((Task.question_answering, Model.distilbert_base_uncased))
class QuestionAnswerTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 1e-5)
        num_train_epochs = train_args.get('num_train_epochs', 2)
        evaluation_strategy = train_args.get('evaluation_strategy', "epoch")
        save_strategy = train_args.get('save_strategy', "epoch")
        per_device_train_batch_size = train_args.get('per_device_train_batch_size', 16)
        gradient_accumulation_steps = train_args.get('gradient_accumulation_steps', 4)
        per_device_eval_batch_size = train_args.get('per_device_eval_batch_size', 16)
        weight_decay = train_args.get('weight_decay', 0.01)
        logging_steps = train_args.get('logging_steps', 10)
        warmup_steps = train_args.get('warmup_steps', 100)
        fp16 = True 
        bf16 = train_args.get('bf16',False)
        if bf16 == True:
            fp16 = False
        
        eval_steps = train_args.get('eval_steps', 200)
        save_steps = train_args.get('save_steps', 200)
        max_steps = train_args.get('max_steps', 5000)
        resume_from_checkpoint = train_args.get('resume_from_checkpoint', False)
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy=evaluation_strategy,
            save_strategy=save_strategy,
            learning_rate=learning_rate,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            num_train_epochs=num_train_epochs,
            weight_decay=weight_decay,
            gradient_accumulation_steps = gradient_accumulation_steps,
            logging_steps = logging_steps,
            warmup_steps = warmup_steps,
            fp16 = fp16,
            bf16= bf16,
            optim="adamw_torch",
            eval_steps = eval_steps,
            save_steps = save_steps,
            max_steps = max_steps,
            push_to_hub=False,
            resume_from_checkpoint="latest_checkpoint",
        )
        logger.info(f'training_args {training_args}')
        trainer = Trainer(
            model=model.model_ins,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            tokenizer=preprocessor.preprocessor_ins,
            data_collator=data_collator.datacollator_ins,
            callbacks=[TrainProgress(train_progress)],
        )
        self.trainer = trainer
        self.model = model.model_ins
        self.output_dir = output_dir
        self.resume_from_checkpoint = resume_from_checkpoint
    
    def train(self):
        from transformers.trainer_utils import get_last_checkpoint
        resume_from_checkpoint = False
        if self.resume_from_checkpoint:
            resume_from_checkpoint = get_last_checkpoint(self.output_dir)
            if resume_from_checkpoint is None:
                resume_from_checkpoint = False
        self.trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        self.model.save_pretrained(self.output_dir)

    def postprocess(self):
        self.trainer.evaluate()



