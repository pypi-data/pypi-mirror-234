
from transformers.data import data_collator
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner import constant 
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.constant import Task, Model

@DataCollatorRg.register((Task.token_classification, Model.distilbert_base_uncased))
class DataCollatorForToken(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)

    def forward(self, **kwargs):
        pass
    
    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor, model:AILabModel) :
        datacollator = data_collator.DataCollatorForTokenClassification(tokenizer=preprocessor.preprocessor_ins,return_tensors=framework)
        return cls(datacollator, preprocessor)