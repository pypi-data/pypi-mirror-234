from typing import Callable
import torch
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@TrainerRg.register((Task.visual_question_answering, Model.vilt))
class ViltTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        from torch.utils.data import DataLoader
        def collate_fn(batch):
            input_ids = [item['input_ids'] for item in batch]
            pixel_values = [item['pixel_values'] for item in batch]
            attention_mask = [item['attention_mask'] for item in batch]
            token_type_ids = [item['token_type_ids'] for item in batch]
            labels = [item['labels'] for item in batch]
            processor = preprocessor.preprocessor_ins
            # create padded pixel values and corresponding pixel mask
            encoding = processor.feature_extractor.pad_and_create_pixel_mask(pixel_values, return_tensors="pt")
            
            # create new batch
            batch = {}
            batch['input_ids'] = torch.stack(input_ids)
            batch['attention_mask'] = torch.stack(attention_mask)
            batch['token_type_ids'] = torch.stack(token_type_ids)
            batch['pixel_values'] = encoding['pixel_values']
            batch['pixel_mask'] = encoding['pixel_mask']
            batch['labels'] = torch.stack(labels)
            return batch
        
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 5e-5)

        dataset = dataset.to_hf_dataset()
        model = model.model_ins
        train_dataloader = DataLoader(dataset, collate_fn=collate_fn, batch_size=4, shuffle=True)
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        self._train_dataloader = train_dataloader
        self._optimizer = optimizer
        self._model = model
        self._output_dir = output_dir
        self.train_progress = train_progress
    
    def train(self):
        train_dataloader = self._train_dataloader
        batch = next(iter(train_dataloader))
        model = self._model
        optimizer = self._optimizer
        accelerator = self.accelerator.accelerator_ins

        train_dataloader, model, optimizer = accelerator.prepare(
                train_dataloader, model, optimizer)
        
        model.train()
        one_step = 0
        for epoch in range(50):  # loop over the dataset multiple times
            logger.info(f"Epoch: {epoch}")
            for batch in self._train_dataloader:
                # zero the parameter gradients
                percent = one_step * 100 / len(self._train_dataloader) / 50
                self.train_progress(percent)
                one_step += 1
                optimizer.zero_grad()

                # forward + backward + optimize
                batch = {k:v.to(torch.device('cuda')) for k,v in batch.items()}
                outputs = model(**batch)
                loss = outputs.loss
                logger.info("Loss:", loss.item())
                #loss.backward()
                accelerator.backward(loss)
                optimizer.step()

        accelerator.wait_for_everyone()
        if accelerator.is_main_process:
            logger.info("is_main_process, save model:",self._output_dir)
            unwrapped_model = accelerator.unwrap_model(model)
            unwrapped_model.save_pretrained(self._output_dir, 
                                            save_function=accelerator.save,
                                            state_dict=accelerator.get_state_dict(model))
        else:
            logger.info("other process")

    def postprocess(self):
        pass



