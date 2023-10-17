from transformers import models
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model

@PreProcessorRg.register((Task.text_classification, Model.distilbert_base_uncased))
class TextClassificationPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)
    
    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        hf_preprocessor = models.auto.AutoProcessor.from_pretrained(pc_name_dir, **kwargs)
        return cls(dataset, hf_preprocessor)
    
    def process_data(self) ->AILabDataset:
        preprocessor = self._preprocessor
        def preprocessor_func(dataset):
            first_sentence = dataset["text"]
            return preprocessor(first_sentence, truncation=True)
        tokenized_dataset = self._dataset.to_hf_dataset().map(preprocessor_func, batched=True)
        return AILabDataset(tokenized_dataset)
