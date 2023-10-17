from typing import List
import torch
from transformers import AutoModelForCausalLM,AutoConfig, BitsAndBytesConfig
from peft import TaskType,LoraConfig,get_peft_model,PeftModel
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.baichuan_7b))
@ModelRg.register((Task.question_answering, Model.baichuan_13b))
@ModelRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@ModelRg.register((Task.question_answering, Model.falcon_7b))
@ModelRg.register((Task.question_answering, Model.moss_moon_003_base))
@ModelRg.register((Task.question_answering, Model.llama2_7b))
@ModelRg.register((Task.question_answering, Model.internlm_7b))
@ModelRg.register((Task.question_answering, Model.belle_7b_2m))
@ModelRg.register((Task.question_answering, Model.xverse_13b))
@ModelRg.register((Task.question_answering, Model.lawgpt_llama))
@ModelRg.register((Task.question_answering, Model.educhat))
class BaichuanModel(AILabModel):
    def __init__(self, model: any) -> None:
        self.model_name = None
        super().__init__(model)

    def forward(self,**kwargs):
        model = self.model_ins
        finetune_type = kwargs['model_args'].get('finetune_type','lora')

        output_embedding_layer_name = "lm_head"
        layer_norm_names = ["norm", "ln_f", "ln_attn", "ln_mlp"]
        for name, param in model.named_parameters():
            if param.ndim == 1 and any(layer_norm_name in name for layer_norm_name in layer_norm_names):
                param.data = param.data.to(torch.float32)

        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()
        else:
            def make_inputs_require_grad(module, input, output):
                output.requires_grad_(True)
            model.get_input_embeddings().register_forward_hook(make_inputs_require_grad)

        model.gradient_checkpointing_enable()
        model.config.use_cache = False # turn off when gradient checkpointing is enabled

        if finetune_type != "full" and hasattr(model, output_embedding_layer_name):
            output_embedding_layer: torch.nn.Linear = getattr(model, output_embedding_layer_name)
            input_dtype = output_embedding_layer.weight.dtype

            class CastOutputToFloat(torch.nn.Sequential):
                def forward(self, x: torch.Tensor) -> torch.Tensor:
                    return super().forward(x.to(input_dtype)).to(torch.float32)

            setattr(model, output_embedding_layer_name, CastOutputToFloat(output_embedding_layer))

        if finetune_type == "full":
            model = model.float()

        if finetune_type == "lora":
            #for dpo
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

            target_modules_dict = {
                Model.baichuan_7b : ['W_pack'],
                Model.baichuan_13b : ['W_pack'],
                Model.bloomz_7b1_mt : ['query_key_value'],
                Model.falcon_7b : ['query_key_value'],
                Model.moss_moon_003_base : ['q_proj','v_proj'],
                Model.llama2_7b : ['q_proj','v_proj'],
                Model.internlm_7b: ['q_proj','v_proj'],
                Model.belle_7b_2m: ['query_key_value'],
                Model.xverse_13b: ['q_proj','v_proj'],
                Model.lawgpt_llama: ['q_proj','v_proj'],
                Model.educhat: ['q_proj','v_proj'],
            }
            
            lora_config = LoraConfig(
                    task_type=TaskType.CAUSAL_LM,
                    inference_mode=False,
                    r=8,
                    lora_alpha=32.0,
                    lora_dropout=0.1,
                    target_modules=target_modules_dict.get(self.model_name),
                )
            model = get_peft_model(model, lora_config)

        def print_trainable_params(model: torch.nn.Module) -> None:
            trainable_params, all_param = 0, 0
            for param in model.parameters():
                num_params = param.numel()
                # if using DS Zero 3 and the weights are initialized empty
                if num_params == 0 and hasattr(param, "ds_numel"):
                    num_params = param.ds_numel
                all_param += num_params
                if param.requires_grad:
                    trainable_params += num_params
            logger.info("trainable params: {:d} || all params: {:d} || trainable%: {:.4f}".format(
                        trainable_params, all_param, 100 * trainable_params / all_param))
        print_trainable_params(model)
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        # quantization args
        quantization_bit = kwargs.get('quantization_bit', None)
        quantization_type = kwargs.get('quantization_type', 'nf4')
        double_quantization = kwargs.get("double_quantization", True)
        compute_dtype = kwargs.get('compute_dtype', torch.float16)
        
        #qlora 的配置参数
        config_kwargs = {"trust_remote_code": True} 

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
            
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_dir,
            config=config,
            torch_dtype=torch.bfloat16 if compute_dtype == torch.bfloat16 else torch.float16,#QLoRA
            low_cpu_mem_usage=True,
            **config_kwargs,
        )

        if hasattr(config, "auto_map") and "AutoConfig" in config.auto_map:
            config.__class__.register_for_auto_class()
        if hasattr(config, "auto_map") and "AutoModelForCausalLM" in config.auto_map:
            model.__class__.register_for_auto_class()
        cls_model =  cls(model)
        cls_model.model_name = model_name
        return cls_model
    
    def get_inside_models(self, model_type:str):
        pass
