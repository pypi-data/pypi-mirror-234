from abc import ABC, abstractmethod
from ailab.atp_evaluation.constant import Task, Model
from ailab.atp_evaluation.build import ModelRg

class AILabModel(ABC):
    def __init__(self, model_name: str, model:any, tokenizer: any, device: str) -> None:
        self._model_name = model_name
        self._model = model
        self._tokenizer = tokenizer
        self._device = device
        self._choices = ["A", "B", "C", "D"]

    @property
    def model_ins(self) :
        return self._model

    @property
    def model_name(self) :
        return self._model_name

    @classmethod
    def from_pretrained(cls, device_name: str, task: Task, model_name: Model, model_dir: str, 
                        lora_weight_dir: str, tokenizer_dir: str, cudaIdx: int, **kwargs) :
        auto_model = ModelRg.get_cls((task, model_name))
        if auto_model is None:
            raise TypeError(f'auto_model is None')
        args = kwargs.get('model_args') or {}
        return auto_model.build_model(device_name, model_name, model_dir, lora_weight_dir, tokenizer_dir, cudaIdx, **args)

    @abstractmethod
    def get_answer_of_multiple_choices_question(self, prompt, choices, do_sample=False, num_beams=1, top_p=0.7, temperature=0.95, logits_processor=None, **kwargs):
        pass