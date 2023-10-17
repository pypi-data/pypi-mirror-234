import os
import argparse, subprocess
from ailab.utils.other import install_requiremet
from ailab.log import logger
from ailab.atp_finetuner.constant import Model

# 最终的参数字典
args_dict = {
    "STAGE": "",
    "PRETRAINED_MODEL_NAME": "",
    "MODEL_NAME": "",
    "DATASET_PATH": "",
    "DATASET_SPLIT":"",
    "PRETRAINED_MODEL_PATH": "",
    "TOKENIZER_PATH": "",
    "OUTPUT_DIR": "",
    "FINETUNE_TYPE": "",
    "DISTRIBUTED": "",
    "NNODES": "",
    "RANK": "",
    "MASTER_ADDR": "",
    "MASTER_PORT": "",
    "NUM_TRAIN_EPOCHS": "",
    "LEARNING_RATE": "",
    "MAX_SOURCE_LENGTH": "",
    "END_TO_ZIP": "",
    "PER_DEVICE_TRAIN_BATCH_SIZE": "",
    "CHECKPOINT_DIR": "",
}


def install_req():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    install_requiremet(dir_path)


def test():
    # 获取当前路径
    current_dir = os.path.dirname(os.path.realpath(__file__))
    train_imp_path = os.path.join(current_dir, "train_imp.py")

    _ = ["MODEL_NAME", "DISTRIBUTED", "NNODES", "RANK", "MASTER_ADDR", "MASTER_PORT"]
    train_imp_args = " ".join([f"--{key} {value}" for key, value in args_dict.items() if key not in _])
    train_imp = f"{train_imp_path} {train_imp_args}"

    gpu_cnt = subprocess.run(["nvidia-smi", "--list-gpus"], stdout=subprocess.PIPE, text=True)
    gpu_cnt = len(gpu_cnt.stdout.strip().split("\n"))
    if args_dict["DISTRIBUTED"] == True:
        if any(temp is None for temp in _[1:]):
            raise SystemExit("NNODES, RANK, MASTER_ADDR, MASTER_PORT not be None")

        torchrun_cmd = f"torchrun --nnodes {args_dict['NNODES']} --nproc_per_node {gpu_cnt} --node_rank {args_dict['RANK']} --master_addr {args_dict['MASTER_ADDR']} --master_port {args_dict['MASTER_PORT']} {train_imp}"
    else:
        torchrun_cmd = f"torchrun --nnodes 1 --nproc_per_node {gpu_cnt} {train_imp}"

    result = subprocess.run(torchrun_cmd, shell=True)

    status = result.returncode
    exit(status)


if __name__ == "__main__":
    # 获取python-- 中的参数
    parser = argparse.ArgumentParser(description="An example script with command-line arguments.")
    parser.add_argument("--stage", dest="STAGE", type=str, default=None)
    parser.add_argument("--pretrained_model_name", dest="PRETRAINED_MODEL_NAME", type=str, default=None)
    parser.add_argument("--model_name", dest="MODEL_NAME", type=str, default=None)
    parser.add_argument("--dataset_path", dest="DATASET_PATH", type=str, default=None)
    parser.add_argument("--pretrained_model_path", dest="PRETRAINED_MODEL_PATH", type=str, default=None)
    parser.add_argument("--tokenizer_path", dest="TOKENIZER_PATH", type=str, default=None)
    parser.add_argument("--output_dir", dest="OUTPUT_DIR", type=str, default=None)
    parser.add_argument("--finetune_type", dest="FINETUNE_TYPE", type=str, default=None)
    parser.add_argument("--distributed", dest="DISTRIBUTED", default=None, help="if use distributed, set True")
    parser.add_argument("--nnodes", dest="NNODES", type=str, default=None)
    parser.add_argument("--rank", dest="RANK", type=str, default=None)
    parser.add_argument("--master_addr", dest="MASTER_ADDR", default=None)
    parser.add_argument("--master_port", dest="MASTER_PORT", default=None)
    parser.add_argument("--num_train_epochs", dest="NUM_TRAIN_EPOCHS", default=None)
    parser.add_argument("--learning_rate", dest="LEARNING_RATE", default=None)
    parser.add_argument("--max_source_length", dest="MAX_SOURCE_LENGTH", default=None)
    parser.add_argument("--end_to_zip", dest="END_TO_ZIP", default=None)
    parser.add_argument("--per_device_train_batch_size", dest="PER_DEVICE_TRAIN_BATCH_SIZE", default=None)
    parser.add_argument("--checkpoint_dir", dest="CHECKPOINT_DIR", default=None)
    parser.add_argument("--dataset_split", dest="DATASET_SPLIT", default=None)
    args = parser.parse_args()

    # 获取环境变量中的参数
    # 参数的默认值在这里设置
    os_arg_dict = {}
    os_arg_dict["STAGE"] = os.environ.get("STAGE", "sft")
    os_arg_dict["PRETRAINED_MODEL_NAME"] = os.environ.get("PRETRAINED_MODEL_NAME", None)
    os_arg_dict["MODEL_NAME"] = os.environ.get("MODEL_NAME", None)
    os_arg_dict["DATASET_PATH"] = os.environ.get("DATASET_PATH", None)
    os_arg_dict["OUTPUT_DIR"] = os.environ.get("OUTPUT_DIR", None)
    os_arg_dict["PRETRAINED_MODEL_PATH"] = os.environ.get("PRETRAINED_MODEL_PATH", None)
    os_arg_dict["TOKENIZER_PATH"] = os.environ.get("TOKENIZER_PATH", None)
    os_arg_dict["FINETUNE_TYPE"] = os.environ.get("FINETUNE_TYPE", "lora")
    os_arg_dict["DISTRIBUTED"] = os.environ.get("DISTRIBUTED", False)
    os_arg_dict["NNODES"] = os.environ.get("NNODES", None)
    os_arg_dict["RANK"] = os.environ.get("RANK", None)
    os_arg_dict["MASTER_ADDR"] = os.environ.get("MASTER_ADDR", None)
    os_arg_dict["MASTER_PORT"] = os.environ.get("MASTER_PORT", None)
    os_arg_dict["NUM_TRAIN_EPOCHS"] = os.environ.get("NUM_TRAIN_EPOCHS", 3)
    os_arg_dict["LEARNING_RATE"] = os.environ.get("LEARNING_RATE", 5e-5)
    os_arg_dict["MAX_SOURCE_LENGTH"] = os.environ.get("MAX_SOURCE_LENGTH", 256)
    os_arg_dict["END_TO_ZIP"] = os.environ.get("END_TO_ZIP", False)
    os_arg_dict["PER_DEVICE_TRAIN_BATCH_SIZE"] = os.environ.get("PER_DEVICE_TRAIN_BATCH_SIZE", 4)
    os_arg_dict["CHECKPOINT_DIR"] = os.environ.get("CHECKPOINT_DIR", None)
    os_arg_dict["DATASET_SPLIT"] = os.environ.get("DATASET_SPLIT", 0.2)

    for env_var in tuple(args_dict.keys()):
        env_var_arg = getattr(args, env_var)  # 优先从 显示传入 提取参数
        if env_var_arg == None:
            env_var_arg = os_arg_dict[env_var]  # 显示传入没有的话，从环境变量中提取参数
        args_dict[env_var] = env_var_arg

    if args_dict["OUTPUT_DIR"] == None:
        args_dict["OUTPUT_DIR"] = f"/work/train_output/{args_dict['MODEL_NAME']}"
    else:
        args_dict["OUTPUT_DIR"] = args_dict["OUTPUT_DIR"]

    llama_list = [Model.alpaca, Model.vicuna, Model.chinese_alpaca]
    if args_dict["PRETRAINED_MODEL_PATH"] == None:
        if args_dict["PRETRAINED_MODEL_NAME"] in llama_list:
            args_dict["PRETRAINED_MODEL_PATH"] = f"/home/.atp/models/llama"
        else:
            args_dict["PRETRAINED_MODEL_PATH"] = f"/home/.atp/models/{args_dict['PRETRAINED_MODEL_NAME']}"

    if args_dict["TOKENIZER_PATH"] == None:
        args_dict["TOKENIZER_PATH"] = f"/home/.atp/models/{args_dict['PRETRAINED_MODEL_NAME']}"

    # 显示用户传入的参数
    logger.info(args_dict)

    # 判断是否支持模型
    model_list = [value for attr_name, value in Model.__dict__.items() if not attr_name.startswith("__")]
    if args_dict["PRETRAINED_MODEL_NAME"] not in model_list:
        raise SystemExit(f"Input model{args_dict['PRETRAINED_MODEL_NAME']} is not yet supported")

    # 修改环境中的包
    install_requiremet(os.path.dirname(__file__))
    if args_dict["PRETRAINED_MODEL_NAME"] == Model.baichuan_13b:
        subprocess.check_call("pip install transformers_stream_generator", shell=True)
    if args_dict["PRETRAINED_MODEL_NAME"] == Model.chinese_alpaca:
        print(f'pip install transformers==4.29.1')
        subprocess.check_call("pip install transformers==4.29.1", shell=True)
    if args_dict["PRETRAINED_MODEL_NAME"] in [Model.chinese_alpaca, Model.alpaca, Model.chinese_alpaca_2]:
        subprocess.check_call("pip install datasets==2.8.0", shell=True)
    if args_dict["PRETRAINED_MODEL_NAME"] == Model.falcon_7b:
        subprocess.check_call("pip install einops", shell=True)
    if args_dict["PRETRAINED_MODEL_NAME"] == Model.chinese_alpaca_2:
        subprocess.check_call("pip install flash-attn", shell=True)

    # chinese_llama_alpaca_2暂时还未支持多机训练
    if args_dict["PRETRAINED_MODEL_NAME"] == "chinese_llama_alpaca" or "chinese_llama_alpaca_2":
        args_dict["DISTRIBUTED"] = False
    test()
