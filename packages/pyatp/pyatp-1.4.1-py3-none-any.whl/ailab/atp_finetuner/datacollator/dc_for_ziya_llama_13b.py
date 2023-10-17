import torch
from dataclasses import dataclass
from typing import Sequence,Dict
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.model import AILabModel

@DataCollatorRg.register((Task.question_answering, Model.ziya_llama_13b))
@dataclass
class DataCollatorForZiyallama13b(AILabDataCollator):
    def __init__(self, datacollator, preprocessor):
        super().__init__(self, preprocessor)

    def __call__(self, instances: Sequence[Dict]) -> Dict[str, torch.Tensor]:
        tokenizer = self._preprocessor.preprocessor_ins

        input_ids, labels = tuple([instance[key] for instance in instances] for key in ("input_ids", "labels"))
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=tokenizer.pad_token_id
        )
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=-100)
        return dict(
            input_ids=input_ids,
            labels=labels,
            attention_mask=input_ids.ne(tokenizer.pad_token_id),
        )
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor,model:AILabModel) :
        return cls(None, preprocessor)