from types import MethodType
import torch
from transformers import AutoModel,AutoConfig,AutoTokenizer,BitsAndBytesConfig
from peft import TaskType,LoraConfig,get_peft_model,PeftModel
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.chatglm_6b))
@ModelRg.register((Task.question_answering, Model.chatglm2_6b))
@ModelRg.register((Task.question_answering, Model.code_geex_2))
@ModelRg.register((Task.question_answering, Model.finGPT_chatglm2_v3))
class ChatglmModel(AILabModel):
    def __init__(self, model: any) -> None:
        self.version = "v1"
        super().__init__(model)

    def forward(self,**kwargs):
        model = self.model_ins
        finetune_type = kwargs['model_args'].get('finetune_type','lora')

        if self.version == "v1":
            output_embedding_base_layer = model
            output_embedding_layer_name = "lm_head"
        elif self.version == "v2":
            model.lm_head = model.transformer.output_layer
            output_embedding_base_layer = model.transformer
            output_embedding_layer_name = "output_layer"

        layer_norm_names = ["layernorm"] # for chatglm setting
        for name, param in model.named_parameters():
            if param.ndim == 1 and any(layer_norm_name in name for layer_norm_name in layer_norm_names):
                param.data = param.data.to(torch.float32)

        model.enable_input_require_grads()
        model.gradient_checkpointing_enable()
        model.config.use_cache = False # turn off when gradient checkpointing is enabled

        if finetune_type != "full" and hasattr(output_embedding_base_layer, output_embedding_layer_name):
            output_embedding_layer = getattr(output_embedding_base_layer, output_embedding_layer_name)
            input_dtype = output_embedding_layer.weight.dtype

            class CastOutputToFloat(torch.nn.Sequential):

                def forward(self, x: torch.Tensor) -> torch.Tensor:
                    return super().forward(x.to(input_dtype)).to(torch.float32)

            setattr(output_embedding_base_layer, output_embedding_layer_name, CastOutputToFloat(output_embedding_layer))

        if finetune_type == "full":
            model = model.float()

        if finetune_type == "lora":
            checkpoints_dir = kwargs['model_args'].get('checkpoint_dir', None)
            if checkpoints_dir is not None:
                checkpoints_dir = checkpoints_dir.split(',')
                for checkpoint in checkpoints_dir:
                    model = PeftModel.from_pretrained(model, checkpoint)
                    model = model.merge_and_unload()

            #resume_from_latest_checkpoint
            resume_from_checkpoint = kwargs['train_args'].get('resume_from_checkpoint', False)
            if resume_from_checkpoint :
                output_dir = kwargs['train_args'].get('output_dir')
                from transformers.trainer_utils import get_last_checkpoint
                latest_checkpoint = get_last_checkpoint(output_dir)
                if latest_checkpoint:
                    logger.info(f"resume train from checkpoint:{latest_checkpoint}")
                    model = PeftModel.from_pretrained(model, latest_checkpoint)
                    model = model.merge_and_unload()
            
            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM, # we should regard ChatGLM as a causal LM
                inference_mode=False,
                r=8,
                lora_alpha=32.0,
                lora_dropout=0.1,
                target_modules=['query_key_value'])
            model = get_peft_model(model, lora_config)
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        # quantization args
        quantization_bit = kwargs.get('quantization_bit',  None)
        quantization_type = kwargs.get('quantization_type', 'nf4')
        double_quantization = kwargs.get("double_quantization", True)
        compute_dtype = kwargs.get('compute_dtype', torch.float16)
        
        config_kwargs = {
            "trust_remote_code": True,
        } 

        model_name_or_dir = model_name if model_dir is None else model_dir
        config = AutoConfig.from_pretrained(model_name_or_dir, trust_remote_code=True)
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
            

        model = AutoModel.from_pretrained(
            model_name_or_dir,
            config=config,
            torch_dtype=torch.bfloat16 if compute_dtype == torch.bfloat16 else torch.float16,#QLoRA
            low_cpu_mem_usage=True,
            **config_kwargs,
        )
        model_ins = cls(model)
        tokenizer  = AutoTokenizer.from_pretrained(model_name_or_dir,use_fast=False,padding_side="left",trust_remote_code=True)
        if tokenizer.eos_token_id == 130005: # ChatGLM-6B
            model_ins.version = "v1"
        elif tokenizer.eos_token_id == 2:
            model_ins.version = "v2" # ChatGLM2-6B
        return model_ins
    
    def get_inside_models(self, model_type:str):
        pass
