import torch
from transformers import CLIPTextModel
from diffusers import DDPMScheduler,AutoencoderKL,UNet2DConditionModel
from diffusers.models.attention_processor import LoRAAttnProcessor
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.text_to_image, Model.stable_diffusion_2_1))
class SDModel(AILabModel):
    def __init__(self, model: any):
        self._noise_scheduler = None
        self._text_encoder = None
        self._vae = None
        self._unet = None
        super().__init__(model)

    def forward(self):
        text_encoder = self._text_encoder
        vae = self._vae
        unet = self._unet
        accelerator = self.accelerator.accelerator_ins

        unet.requires_grad_(False)
        vae.requires_grad_(False)
        text_encoder.requires_grad_(False)
        # For mixed precision training we cast the text_encoder and vae weights to half-precision
        # as these models are only used for inference, keeping weights in full precision is not required.
        weight_dtype = torch.float16

        # Move unet, vae and text_encoder to device and cast to weight_dtype
        unet.to(accelerator.device, dtype=weight_dtype)
        vae.to(accelerator.device, dtype=weight_dtype)
        text_encoder.to(accelerator.device, dtype=weight_dtype)

        # Set correct lora layers
        lora_attn_procs = {}
        for name in unet.attn_processors.keys():
            cross_attention_dim = None if name.endswith("attn1.processor") else unet.config.cross_attention_dim
            if name.startswith("mid_block"):
                hidden_size = unet.config.block_out_channels[-1]
            elif name.startswith("up_blocks"):
                block_id = int(name[len("up_blocks.")])
                hidden_size = list(reversed(unet.config.block_out_channels))[block_id]
            elif name.startswith("down_blocks"):
                block_id = int(name[len("down_blocks.")])
                hidden_size = unet.config.block_out_channels[block_id]

            lora_attn_procs[name] = LoRAAttnProcessor(hidden_size=hidden_size, cross_attention_dim=cross_attention_dim)

        unet.set_attn_processor(lora_attn_procs)
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        noise_scheduler = DDPMScheduler.from_pretrained(model_name_or_dir, subfolder="scheduler")
        text_encoder = CLIPTextModel.from_pretrained(
            model_name_or_dir, subfolder="text_encoder"
        )
        vae = AutoencoderKL.from_pretrained(model_name_or_dir, subfolder="vae")
        unet = UNet2DConditionModel.from_pretrained(
            model_name_or_dir, subfolder="unet"
        )
        sd_cls = cls(unet)
        sd_cls._noise_scheduler = noise_scheduler
        sd_cls._text_encoder = text_encoder
        sd_cls._vae = vae
        sd_cls._unet = unet
        return sd_cls
    
    def get_inside_models(self, model_type:str):
        if model_type == "noise_scheduler":
            return self._noise_scheduler
        elif model_type == "text_encoder":
            return self._text_encoder
        elif model_type == "vae":
            return self._vae
        elif model_type == "unet":
            return self._unet
        else :
            return None
