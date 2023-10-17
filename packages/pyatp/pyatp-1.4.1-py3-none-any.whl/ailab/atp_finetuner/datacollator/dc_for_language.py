from transformers.data import data_collator
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner import constant 
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.constant import Task, Model

@DataCollatorRg.register((Task.question_answering, Model.vicuna))
@DataCollatorRg.register((Task.question_answering, Model.open_llama))
class DataCollatorForLanguage(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)

    def forward(self, **kwargs):
        pass
    
    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor, model:AILabModel) :
        datacollator = data_collator.DataCollatorForLanguageModeling(
            preprocessor.preprocessor_ins, mlm=False
        )
        return cls(datacollator, preprocessor)