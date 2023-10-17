import os
import torch
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_dataset.constant import Sources
from ailab.atp_finetuner.constant import Task, Framework
from ailab.atp_finetuner.finetuner import AILabFinetuner

def train_progress(percent: float):
    pass

def falcon_test():
    # todo     # fixed pretrained in train_deprecatied.py
    pretrained_model_name = os.environ.get("PRETRAINED_MODEL_NAME","falcon-7b")
    model_name = os.environ.get("MODEL_NAME","")
    dataset_path = os.environ.get("DATASET_PATH")
    output_dir = os.environ.get("OUTPUT_DIR", f"/work/train_output/{model_name}")
    pretrained_model_path = os.environ.get("PRETRAINED_MODEL_PATH", f"/home/.atp/models/{pretrained_model_name}")
    tokenizer_path = os.environ.get("TOKENIZER_PATH", f"/home/.atp/models/{pretrained_model_name}")
    finetune_type=os.environ.get("FINETUNE_TYPE","lora")
    if not model_name or not dataset_path:
        raise TypeError(
            f'os.environ should have (MODEL_NAME,DATASET_PATH)')

    dataset = AILabDataset.load_dataset(dataset_path, src=Sources.huggingface)
    args = {
        "model_args": {
            "quantization_bit": None, # LoRA
        },
        "train_args": {
            "output_dir": output_dir,
            "save_strategy": "steps",
            "learning_rate": float(os.environ.get("LEARNING_RATE",  1e-4)),
            "per_device_train_batch_size": 4,
            "gradient_accumulation_steps": 4,
            "num_train_epochs": int(os.environ.get("NUM_TRAIN_EPOCHS",  4)),
            "logging_steps": 10,
            "fp16": True,
            "bf16": False,
            "optim": os.environ.get("OPTIM",  "adamw_torch"),
            "save_steps": 1000,
            "resume_from_checkpoint": True,
        },
    }
    if finetune_type=="qlora":
        args["model_args"]["quantization_bit"] = 4
        args["model_args"]["quantization_type"] = "nf4"
        args["model_args"]["double_quantization"] = True
        args["model_args"]["compute_dtype"] =torch.float16
    finetuner = AILabFinetuner(Task.question_answering, Framework.Pytorch, dataset,
                               pretrained_model_name, train_progress,
                               pretrained_model_path,
                               tokenizer_path,
                               **args)
    finetuner.finetuner()


if __name__ == '__main__':
    falcon_test()
