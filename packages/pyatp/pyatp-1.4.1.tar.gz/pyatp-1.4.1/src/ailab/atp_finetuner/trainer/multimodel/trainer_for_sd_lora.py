from typing import Callable
import torch
import math
import os
import numpy as np
from tqdm.auto import tqdm
import torch.nn.functional as F
from diffusers.loaders import AttnProcsLayers
from diffusers.optimization import get_scheduler
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@TrainerRg.register((Task.text_to_image, Model.stable_diffusion_2_1))
class SDTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        self.train_args = train_args
        self.dataset = dataset
        self.model = model
        self.train_progress = train_progress
    
    def train(self):
        weight_dtype = torch.float16
        dataloader_num_workers = 8
        lr_warmup_steps = 0
        max_train_steps = 5000
        lr_scheduler = "cosine"
        train_batch_size = 1
        validation_epochs = 1
        validation_prompt = "Totoro"
        max_grad_norm = 1
        checkpointing_steps = 500
        num_validation_images = 4
        train_args = self.train_args
        model = self.model
        dataset = self.dataset

        learning_rate = train_args.get('learning_rate', 1e-5)
        gradient_accumulation_steps = train_args.get('gradient_accumulation_steps', 4)
        output_dir = train_args.get('output_dir', "./my_sd_model")
        resume_from_checkpoint = train_args.get('resume_from_checkpoint', False)
        text_encoder = model.get_inside_models('text_encoder')
        unet = model.get_inside_models('unet')
        vae = model.get_inside_models('vae')
        noise_scheduler = model.get_inside_models('noise_scheduler')
        train_dataset = dataset.to_hf_dataset()
        accelerator = self.accelerator.accelerator_ins

        lora_layers = AttnProcsLayers(unet.attn_processors)
        optimizer_cls = torch.optim.AdamW
        optimizer = optimizer_cls(
            lora_layers.parameters(),
            lr=learning_rate,
            betas=(0.9, 0.999),
            weight_decay=1e-2,
            eps=1e-08,
        )

        def collate_fn(examples):
            pixel_values = torch.stack([example["pixel_values"] for example in examples])
            pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
            input_ids = torch.stack([example["input_ids"] for example in examples])
            return {"pixel_values": pixel_values, "input_ids": input_ids}

        # DataLoaders creation:
        train_dataloader = torch.utils.data.DataLoader(
            train_dataset,
            shuffle=True,
            collate_fn=collate_fn,
            batch_size=train_batch_size,
            num_workers=dataloader_num_workers,
        )

        # Scheduler and math around the number of training steps.
        num_update_steps_per_epoch = math.ceil(len(train_dataloader) / gradient_accumulation_steps)

        lr_scheduler = get_scheduler(
            lr_scheduler,
            optimizer=optimizer,
            num_warmup_steps=lr_warmup_steps * gradient_accumulation_steps,
            num_training_steps=max_train_steps * gradient_accumulation_steps,
        )

        # Prepare everything with our `accelerator`.
        lora_layers, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
            lora_layers, optimizer, train_dataloader, lr_scheduler
        )

        # We need to recalculate our total training steps as the size of the training dataloader may have changed.
        num_update_steps_per_epoch = math.ceil(len(train_dataloader) / gradient_accumulation_steps)
        # Afterwards we recalculate our number of training epochs
        num_train_epochs = math.ceil(max_train_steps / num_update_steps_per_epoch)

        # We need to initialize the trackers we use, and also store our configuration.
        # The trackers initializes automatically on the main process.
        if accelerator.is_main_process:
            accelerator.init_trackers("text2image-fine-tune")
        

        total_batch_size = train_batch_size * accelerator.num_processes * gradient_accumulation_steps

        logger.info("***** Running training *****")
        logger.info(f"  Num examples = {len(train_dataset)}")
        logger.info(f"  Num Epochs = {num_train_epochs}")
        logger.info(f"  Instantaneous batch size per device = {train_batch_size}")
        logger.info(f"  Total train batch size (w. parallel, distributed & accumulation) = {total_batch_size}")
        logger.info(f"  Gradient Accumulation steps = {gradient_accumulation_steps}")
        logger.info(f"  Total optimization steps = {max_train_steps}")
        global_step = 0
        first_epoch = 0

        if resume_from_checkpoint:
            # Get the most recent checkpoint
            # Get the most recent checkpoint
            dirs = os.listdir(output_dir)
            dirs = [d for d in dirs if d.startswith("checkpoint")]
            dirs = sorted(dirs, key=lambda x: int(x.split("-")[1]))
            path = dirs[-1] if len(dirs) > 0 else None

            if path is None:
                resume_from_checkpoint = None
            else:
                logger.info(f"Resuming from checkpoint {resume_from_checkpoint}")
                accelerator.load_state(os.path.join(output_dir, path))
                global_step = int(path.split("-")[1])

                resume_global_step = global_step * gradient_accumulation_steps
                first_epoch = global_step // num_update_steps_per_epoch
                resume_step = resume_global_step % (num_update_steps_per_epoch * gradient_accumulation_steps)

        # Only show the progress bar once on each machine.
        progress_bar = tqdm(range(global_step, max_train_steps), disable=not accelerator.is_local_main_process)
        progress_bar.set_description("Steps")

        for epoch in range(first_epoch, num_train_epochs):
            unet.train()
            train_loss = 0.0
            for step, batch in enumerate(train_dataloader):
                if resume_from_checkpoint and epoch == first_epoch and step < resume_step:
                    continue

                with accelerator.accumulate(unet):
                    # Convert images to latent space
                    latents = vae.encode(batch["pixel_values"].to(dtype=weight_dtype)).latent_dist.sample()
                    latents = latents * vae.config.scaling_factor

                    # Sample noise that we'll add to the latents
                    noise = torch.randn_like(latents)

                    bsz = latents.shape[0]
                    # Sample a random timestep for each image
                    timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device)
                    timesteps = timesteps.long()

                    # Add noise to the latents according to the noise magnitude at each timestep
                    # (this is the forward diffusion process)
                    noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

                    # Get the text embedding for conditioning
                    encoder_hidden_states = text_encoder(batch["input_ids"])[0]

                    # Get the target for loss depending on the prediction type
                    if noise_scheduler.config.prediction_type == "epsilon":
                        target = noise
                    elif noise_scheduler.config.prediction_type == "v_prediction":
                        target = noise_scheduler.get_velocity(latents, noise, timesteps)
                    else:
                        raise ValueError(f"Unknown prediction type {noise_scheduler.config.prediction_type}")

                    # Predict the noise residual and compute loss
                    model_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample
                    loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")

                    # Gather the losses across all processes for logging (if we use distributed training).
                    avg_loss = accelerator.gather(loss.repeat(train_batch_size)).mean()
                    train_loss += avg_loss.item() / gradient_accumulation_steps

                    # Backpropagate
                    accelerator.backward(loss)
                    if accelerator.sync_gradients:
                        params_to_clip = lora_layers.parameters()
                        accelerator.clip_grad_norm_(params_to_clip, max_grad_norm)
                    optimizer.step()
                    lr_scheduler.step()
                    optimizer.zero_grad()

                # Checks if the accelerator has performed an optimization step behind the scenes
                if accelerator.sync_gradients:
                    progress_bar.update(1)
                    global_step += 1
                    self.train_progress(global_step * 100 / max_train_steps)
                    accelerator.log({"train_loss": train_loss}, step=global_step)
                    train_loss = 0.0

                    if global_step % checkpointing_steps == 0:
                        if accelerator.is_main_process:
                            save_path = os.path.join(output_dir, f"checkpoint-{global_step}")
                            accelerator.save_state(save_path)
                            logger.info(f"Saved state to {save_path}")

                logs = {"step_loss": loss.detach().item(), "lr": lr_scheduler.get_last_lr()[0]}
                progress_bar.set_postfix(**logs)

                if global_step >= max_train_steps:
                    break

            if accelerator.is_main_process:
                torch.cuda.empty_cache()

        # Save the lora layers
        accelerator.wait_for_everyone()
        if accelerator.is_main_process:
            unet = unet.to(torch.float32)
            unet.save_attn_procs(output_dir)

    def postprocess(self):
        pass



