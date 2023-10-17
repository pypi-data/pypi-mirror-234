from typing import List
import torch
from peft import LoraConfig,get_peft_model,prepare_model_for_int8_training
from transformers import LlamaForCausalLM,AutoConfig, BitsAndBytesConfig
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.alpaca))
@ModelRg.register((Task.question_answering, Model.vicuna))
@ModelRg.register((Task.question_answering, Model.open_llama))
@ModelRg.register((Task.question_answering, Model.bencao_llama))
class LoraModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        model = self._model
        model = prepare_model_for_int8_training(model)
        lora_r: int = 8
        lora_alpha: int = 16
        lora_dropout: float = 0.05
        lora_target_modules: List[str] = [
            "q_proj",
            "v_proj",
        ] 

        config = LoraConfig(
            r=lora_r,
            lora_alpha=lora_alpha,
            target_modules=lora_target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, config)
        model.print_trainable_parameters()
        model.is_parallelizable = True
        model.model_parallel = True
        self._model = model
    
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
            
        model = LlamaForCausalLM.from_pretrained(model_name_or_dir,
            from_tf=bool(".ckpt" in model_name_or_dir),
            config=config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True)
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
