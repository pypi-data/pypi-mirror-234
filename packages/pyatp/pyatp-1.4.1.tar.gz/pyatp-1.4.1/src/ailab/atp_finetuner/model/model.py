from abc import ABC,abstractclassmethod
from ailab.atp_finetuner.constant import Task,Model
from ailab.atp_finetuner.build import ModelRg

class AILabModel(ABC):
    def __init__(self,model:any) -> None:
        self._model = model

    @property
    def model_ins(self) :
        return self._model
    
    @property
    def accelerator(self):
        return self._accelerator

    @accelerator.setter
    def accelerator(self, value):
        self._accelerator = value
    
    @classmethod
    def from_pretrained(cls, device_name:str, task: Task, model_name:Model, model_dir:str, **kwargs) :
        auto_model = ModelRg.get_cls((task, model_name))
        if auto_model is None:
            raise TypeError(f'auto_model is None')
        args = kwargs['model_args']
        return auto_model.build_model(device_name, model_name, model_dir, **args)
    
    @abstractclassmethod
    def forward(self, **kwargs):
        pass

    @abstractclassmethod
    def get_inside_models(self, model_type:str):
        pass

    
    