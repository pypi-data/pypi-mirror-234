import os
import subprocess
import sys
from ailab.log import logger


def install_requiremet(basedir: str):
    basereqs = os.path.join(basedir, "requirements.txt")
    if not os.path.exists(basereqs):
        return
    cmd = "pip install -r  " + basereqs
    print(f"executing {cmd}")

    subprocess.call(cmd, shell=True)


from typing import Dict, List, Optional
import os, json, torch
from transformers.trainer import TRAINER_STATE_NAME

VALUE_HEAD_FILE_NAME = "value_head.bin"


def get_state_dict(model: torch.nn.Module) -> Dict[str, torch.Tensor]:  # get state dict containing trainable parameters
    state_dict = model.state_dict()
    filtered_state_dict = {}

    for k, v in model.named_parameters():
        if v.requires_grad:
            filtered_state_dict[k] = state_dict[k].cpu().clone().detach()
    return filtered_state_dict


def load_trainable_params(model: torch.nn.Module, checkpoint_dir: os.PathLike) -> bool:
    from peft.utils.other import WEIGHTS_NAME
    weights_file = os.path.join(checkpoint_dir, WEIGHTS_NAME)
    if not os.path.exists(weights_file):
        logger.info("Provided path ({}) does not contain pre-trained weights.".format(checkpoint_dir))
        return False
    model_state_dict = torch.load(weights_file, map_location="cpu")
    model.load_state_dict(model_state_dict, strict=False)  # skip missing keys
    return True


def load_valuehead_params(model: torch.nn.Module, checkpoint_dir: os.PathLike) -> bool:
    valuehead_file = os.path.join(checkpoint_dir, VALUE_HEAD_FILE_NAME)
    if not os.path.exists(valuehead_file):
        logger.info("Provided path ({}) does not contain valuehead weights.".format(checkpoint_dir))
        return False
    valuehead_state_dict = torch.load(valuehead_file, map_location="cpu")
    model.register_buffer("reward_head_weight", valuehead_state_dict["summary.weight"])
    model.register_buffer("reward_head_bias", valuehead_state_dict["summary.bias"])
    model.register_buffer("default_head_weight", torch.zeros_like(valuehead_state_dict["summary.weight"]))
    model.register_buffer("default_head_bias", torch.zeros_like(valuehead_state_dict["summary.bias"]))
    return True


def smooth(scalars: List[float], weight: Optional[float] = 0.9) -> List[float]:
    r"""
    EMA implementation according to TensorBoard.
    """
    last = scalars[0]
    smoothed = list()
    for next_val in scalars:
        smoothed_val = last * weight + (1 - weight) * next_val
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed


def plot_loss(save_dictionary: os.PathLike, keys: Optional[List[str]] = ["loss"]) -> None:
    import matplotlib.pyplot as plt
    with open(os.path.join(save_dictionary, TRAINER_STATE_NAME), "r", encoding="utf-8") as f:
        data = json.load(f)

    for key in keys:
        steps, metrics = [], []
        for i in range(len(data["log_history"])):
            if key in data["log_history"][i]:
                steps.append(data["log_history"][i]["step"])
                metrics.append(data["log_history"][i][key])

        if len(metrics) == 0:
            logger.info(f"No metric {key} to plot.")
            continue

        plt.figure()
        plt.plot(steps, metrics, alpha=0.4, label="original")
        plt.plot(steps, smooth(metrics), label="smoothed")
        plt.title("training {} of {}".format(key, save_dictionary))
        plt.xlabel("step")
        plt.ylabel(key)
        plt.legend()
        plt.savefig(os.path.join(save_dictionary, "training_{}.png".format(key)), format="png", dpi=100)
        logger.info("Figure saved:", os.path.join(save_dictionary, "training_{}.png".format(key)))


import os
import zipfile
import shutil


def create_zip_and_delete_folder(folder_path, zip_path):
    try:
        files_to_compress = ['adapter_model.bin', 'adapter_config.json']  # 要压缩的文件列表

        # 创建一个 ZIP 文件并添加文件到其中
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name in files_to_compress:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))

        # 删除 checkpoint-* 文件
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for dirname in dirnames:
                if dirname.startswith("checkpoint-"):
                    dir_to_delete = os.path.join(dirpath, dirname)
                    print(f"Deleting directory: {dir_to_delete}")
                    shutil.rmtree(dir_to_delete)
        
        # 删除 runs 文件夹
        runs_folder = os.path.join(folder_path, "runs")
        if os.path.exists(runs_folder):
            shutil.rmtree(runs_folder)

        print(f"文件夹 '{folder_path}' 已打包为 '{zip_path}' 并删除其他文件")
    except Exception as e:
        print(f"发生错误：{e}")
