import os
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_dataset.constant import Sources
from ailab.atp_finetuner.constant import Task, Framework
from ailab.atp_finetuner.finetuner import AILabFinetuner
from ailab.utils.other import install_requiremet

def train_progress(percent: float):
    pass

def install_req():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    install_requiremet(dir_path)


def open_llama_test():
    # todo     # fixed pretrained in train_deprecatied.py
    pretrained_model_name = os.environ.get("PRETRAINED_MODEL_NAME","open_llama_7b")
    model_name = os.environ.get("MODEL_NAME","")
    dataset_path = os.environ.get("DATASET_PATH")
    output_dir = os.environ.get("OUTPUT_DIR", f"/work/train_output/{model_name}")
    pretrained_model_path = os.environ.get("PRETRAINED_MODEL_PATH", f"/home/.atp/models/{pretrained_model_name}")
    tokenizer_path = os.environ.get("TOKENIZER_PATH", f"/home/.atp/models/{pretrained_model_name}")

    if  not dataset_path:
        raise TypeError(
            f'os.environ should have (DATASET_PATH)')

    dataset = AILabDataset.load_dataset(dataset_path, src=Sources.huggingface)
    dataset.train_test_split(test_size=0.2)
    args = {
        "model_args": {
        },
        "train_args": {
            "output_dir": output_dir,
            "evaluation_strategy": "steps",
            "save_strategy": "steps",
            "learning_rate": float(os.environ.get("LEARNING_RATE",  3e-4)),
            "per_device_train_batch_size": 16,
            "gradient_accumulation_steps": 4,
            "per_device_eval_batch_size": 16,
            "num_train_epochs": int(os.environ.get("NUM_TRAIN_EPOCHS",  3)),
            "weight_decay": 0.01,
            "logging_steps": 10,
            "warmup_steps": 100,
            "fp16": True,
            "optim": os.environ.get("OPTIM",  "adamw_torch"),
            "eval_steps": 200,
            "save_steps": 200,
            "resume_from_checkpoint": True,
        },
    }
    finetuner = AILabFinetuner(Task.question_answering, Framework.Pytorch, dataset,
                               pretrained_model_name, train_progress,
                               pretrained_model_path,
                               tokenizer_path,
                               **args)
    finetuner.finetuner()


if __name__ == '__main__':
    install_req()
    open_llama_test()
