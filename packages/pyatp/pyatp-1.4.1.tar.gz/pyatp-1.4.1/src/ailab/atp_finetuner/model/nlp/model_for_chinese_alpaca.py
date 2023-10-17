from typing import List
import torch
from transformers import LlamaForCausalLM,AutoConfig, BitsAndBytesConfig
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.chinese_alpaca))
@ModelRg.register((Task.question_answering, Model.chinese_alpaca_2))
class ChineseAlpacaModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self,**kwargs):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        # quantization args
        quantization_bit = kwargs.get('quantization_bit',  None)
        quantization_type = kwargs.get('quantization_type', 'nf4')
        double_quantization = kwargs.get("double_quantization", True)
        compute_dtype = kwargs.get('compute_dtype', torch.float16)
        
        config_kwargs = {} 

        model_name_or_dir = model_name if model_dir is None else model_dir

        config = AutoConfig.from_pretrained(model_name_or_dir)
        quantization_bit = None # Temporarily disabling qlora for erroneous inference results
        # Quantization configurations (using bitsandbytes library).
        if quantization_bit is not None:
            if quantization_bit == 8:
                config_kwargs["load_in_8bit"] = True
                config_kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_8bit=True,
                )

            elif quantization_bit == 4:
                config_kwargs["load_in_4bit"] = True
                config_kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=compute_dtype,
                    bnb_4bit_use_double_quant=double_quantization,
                    bnb_4bit_quant_type=quantization_type
                )

            logger.info("Quantizing model to {} bit.".format(quantization_bit))

        model = LlamaForCausalLM.from_pretrained(
            model_name_or_dir,
            from_tf=bool(".ckpt" in model_name_or_dir),
            config=config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            **config_kwargs
        )
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
