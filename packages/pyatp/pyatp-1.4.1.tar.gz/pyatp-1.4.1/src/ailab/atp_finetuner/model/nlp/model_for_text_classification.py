from ailab.atp_finetuner.model.model import AILabModel
from transformers.models import auto
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.text_classification, Model.distilbert_base_uncased))
class TextClassificationModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        model = auto.AutoModelForSequenceClassification.from_pretrained(model_name_or_dir, **kwargs)
        model.to(device_name)
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
