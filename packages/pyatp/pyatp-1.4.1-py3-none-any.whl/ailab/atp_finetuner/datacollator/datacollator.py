from abc import ABC, abstractmethod
from transformers.data import data_collator 
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.constant import Task, Model, Framework
from ailab.atp_finetuner.build import DataCollatorRg

class AILabDataCollator(ABC):
    def __init__(self, datacollator, preprocessor) :
        self._datacollator = datacollator
        self._preprocessor = preprocessor
    
    @property
    def datacollator_ins(self):
        return self._datacollator
    
    @property
    def preprocessor_ins(self):
        return self._preprocessor

    @classmethod
    def from_task_model(cls, task_name:Task, model_name:Model, 
                        framework:Framework, preprocessor:AILabPreprocessor,
                        model:AILabModel) :
        auto_data_collator = DataCollatorRg.get_cls((task_name, model_name))
        if auto_data_collator is None:
            return DataCollatorForDefault.build_datacollator(framework, preprocessor)
        return auto_data_collator.build_datacollator(framework, preprocessor, model)
    
    @abstractmethod
    def forward(self, **kwargs) :
        pass

class DataCollatorForDefault(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)

    def forward(self, **kwargs):
        pass
    
    @classmethod
    def build_datacollator(cls, framework:Framework, preprocessor:AILabPreprocessor) :
        datacollator = data_collator.DefaultDataCollator(return_tensors=framework)
        return cls(datacollator, preprocessor)
