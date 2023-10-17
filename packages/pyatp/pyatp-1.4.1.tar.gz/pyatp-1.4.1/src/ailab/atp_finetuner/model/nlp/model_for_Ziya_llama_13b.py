from typing import List
import torch
import os
from transformers import LlamaForCausalLM,AutoConfig,AutoModelForCausalLM,BitsAndBytesConfig
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.ziya_llama_13b))
class ZiyallamaModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self,**kwargs):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir

        # torch_dtype=torch.float16
        # config = AutoConfig.from_pretrained(model_name_or_dir)
        # 加载模型
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_dir,
            #device_map="auto",
            load_in_4bit=True,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                llm_int8_threshold=6.0,
                llm_int8_has_fp16_weight=False,
            ),
        )
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass