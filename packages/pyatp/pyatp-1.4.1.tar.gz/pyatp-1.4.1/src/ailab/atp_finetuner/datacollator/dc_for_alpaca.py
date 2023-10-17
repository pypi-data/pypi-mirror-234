from transformers.data import data_collator
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.constant import Task, Model


@DataCollatorRg.register((Task.question_answering, Model.alpaca))
@DataCollatorRg.register((Task.question_answering, Model.bencao_llama))
class DataCollatorForAlpaca(AILabDataCollator):
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)

    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework: constant.Framework, preprocessor: AILabPreprocessor, model:AILabModel):
        datacollator = data_collator.DataCollatorForSeq2Seq(
            preprocessor.preprocessor_ins, pad_to_multiple_of=8, return_tensors=framework, padding=True
        )
        return cls(datacollator, preprocessor)
