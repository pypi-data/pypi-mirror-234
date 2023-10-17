import os
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_dataset.constant import Sources
from ailab.atp_finetuner.constant import Task, Framework
from ailab.atp_finetuner.finetuner import AILabFinetuner

def train_progress(percent: float):
    pass


def ziya_llama_13b_test():
    # todo     # fixed pretrained in train_deprecatied.py
    pretrained_model_name = os.environ.get("PRETRAINED_MODEL_NAME")
    model_name = os.environ.get("MODEL_NAME")
    dataset_path = os.environ.get("DATASET_PATH")
    output_dir = os.environ.get("OUTPUT_DIR", f"/work/model/{model_name}")
    pretrained_model_path = os.environ.get("PRETRAINED_MODEL_PATH")
    tokenizer_path = os.environ.get("TOKENIZER_PATH")

    if not model_name or not dataset_path or not tokenizer_path:
        raise TypeError(
            f'os.environ should have (MODEL_NAME,DATASET_PATH,TOKENIZER_PATH)')

    dataset = AILabDataset.load_dataset(dataset_path, src=Sources.huggingface)
    dataset.train_test_split(test_size=0.2)
    args = {
        "model_args": {
        },
        "train_args": {
            "output_dir": output_dir,
            "evaluation_strategy": "epoch",  
            "per_device_eval_batch_size": 4,          
            "eval_steps": 250,
            "resume_from_checkpoint": False,
            "num_train_epochs": int(os.environ.get("NUM_TRAIN_EPOCHS",  3)),
            "per_device_train_batch_size": 4,
            "gradient_accumulation_steps": 4,
            "learning_rate": float(os.environ.get("LEARNING_RATE",  1e-4)),
            "logging_steps": 300,
            "save_steps": 500,
            "fp16": True,
            "save_strategy": "steps",
            "weight_decay": 0,
        },
    }
    finetuner = AILabFinetuner(Task.question_answering, Framework.Pytorch, dataset,
                               pretrained_model_name, train_progress,
                               pretrained_model_path,
                               tokenizer_path,
                               **args)
    finetuner.finetuner()


if __name__ == '__main__':
    ziya_llama_13b_test()
