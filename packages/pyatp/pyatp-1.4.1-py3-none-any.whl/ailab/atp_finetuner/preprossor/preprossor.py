from abc import ABC, abstractmethod
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.constant import Task,Model
from ailab.atp_finetuner.build import PreProcessorRg

class AILabPreprocessor(ABC) :
    def __init__(self, dataset, hf_preprocessor):
        self._preprocessor = hf_preprocessor
        self._dataset = dataset
        self._accelerator = None
        self._max_source_length = 512

    @property
    def preprocessor_ins(self):
        return self._preprocessor
    
    @property
    def accelerator(self):
        return self._accelerator

    @accelerator.setter
    def accelerator(self, value):
        self._accelerator = value
    
    @classmethod
    def from_pretrained(cls, task:Task, model_name:Model, dataset: AILabDataset, pc_dir:str, **kwargs) :
        auto_preprocessor = PreProcessorRg.get_cls((task, model_name))
        if auto_preprocessor is None:
            raise TypeError(f'auto_preprocessor is None')
        return auto_preprocessor.build_preprocessor(model_name, dataset, pc_dir, **kwargs)
    
    @abstractmethod
    def process_data(self) ->AILabDataset:
        pass

    def process_rm_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        dataset = self._dataset.to_hf_dataset()

        def preprocess_pairwise_dataset(examples):
            return {"prompt" : examples["prompt"],
                    "chosen" : examples["chosen"],
                    "rejected" : examples["rejected"]}

        tokenized_dataset = dataset.map(preprocess_pairwise_dataset,
                                        batched=True,)
        return AILabDataset(tokenized_dataset)



        