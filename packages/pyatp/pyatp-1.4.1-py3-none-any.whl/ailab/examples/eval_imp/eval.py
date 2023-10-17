
import json
import os
import argparse

import numpy as np
from ailab.atp_evaluation.constant import BenchMarkType, Model
from ailab.atp_evaluation.evaluator import AILabEvaluator

METRICS = ["acc_norm", "acc_norm", "acc", "mc2"]
BENCHMARKS = ["arc_challenge", "hellaswag", "hendrycksTest", "truthfulqa_mc"]
BENCH_TO_NAME = {
    "arc_challenge": "ARC",
    "hellaswag": "HellaSwag",
    "hendrycksTest": "MMLU",
    "truthfulqa_mc": "TruthfulQA",
}

def validate_enum_value(cls, value):
    attrs = [attr for attr in dir(cls) if not attr.startswith('__')]
    if value not in attrs:
        raise argparse.ArgumentTypeError(f"Invalid value {value}. Must be one of \"{', '.join(attrs)}\".")
    return value

def validate_file_path(hint, path):
    # 规范化路径
    if not os.path.exists(path):
        raise ValueError("Invalid {} path: {}".format(hint, path))

def delete_files_with_keyword(folder_path, file_name):
    # 确保文件夹存在
    if not os.path.exists(folder_path):
        return
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

def get_fewshot_num(benchmark_type:BenchMarkType):
    ntrain = 0
    if benchmark_type == BenchMarkType.arc_challenge:
        ntrain = 25
    elif benchmark_type == BenchMarkType.hellaswag:
        ntrain = 10
    elif (benchmark_type == BenchMarkType.mmlu
            or benchmark_type == BenchMarkType.ceval_validation
            or benchmark_type == BenchMarkType.cmmlu):
        ntrain = 5
    elif benchmark_type == BenchMarkType.private:
        ntrain = 3
    return ntrain

def get_task_eval_file_name(model:Model, is_peft:bool, task_attr_name:str):
    ntrain = get_fewshot_num(getattr(BenchMarkType, task_attr_name))
    outfile = f"{model}_{task_attr_name}_{ntrain}s.json"
    if is_peft:
        outfile = f"{model}_peft_{task_attr_name}_{ntrain}s.json"
    return outfile

def update_result(result:dict, folder_path:str, file_name:str):
    task_eval_file = os.path.join(folder_path, file_name)
    with open(task_eval_file) as fp:
        data = json.load(fp)
    for benchmark, metric in zip(BENCHMARKS, METRICS):
        accs = np.array([v[metric] for k, v in data["results"].items() if benchmark in k])
        if accs.size == 0:
            continue
        mean_acc = np.mean(accs) * 100.0
        result[BENCH_TO_NAME[benchmark]]=round(mean_acc, 2)
        print("update:", BENCH_TO_NAME[benchmark])

if __name__ == "__main__":
    # 获取python-- 中的参数
    parser = argparse.ArgumentParser(description="Run an evaluation task")
    parser.add_argument("--pretrained_model_name", type=str, required=True)
    parser.add_argument("--pretrained_model_path", type=str, required=True)
    parser.add_argument("--tokenizer_path", type=str, nargs='?', default=None)
    parser.add_argument("--finetuned_weight_path", nargs='?', type=str, default=None)
    parser.add_argument("--dataset_path", type=str, required=True)
    parser.add_argument("--benchmarks", 
                        help='benchmarks to evaluate for this task',
                        type=str, 
                        default="truthfulqa_mc,arc_challenge,hellaswag,mmlu")
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()

    # 检测pretrained_model_name中字符串的合法性
    validate_enum_value(Model, args.pretrained_model_name)

    # 检测路径合法性
    validate_file_path("--pretrained_model_path", args.pretrained_model_path)
    if args.tokenizer_path == "":
        args.tokenizer_path = None
    if args.tokenizer_path is not None:
        validate_file_path("--tokenizer_path", args.tokenizer_path)
    if args.finetuned_weight_path == "":
        args.finetuned_weight_path = None
    if args.finetuned_weight_path is not None:
        validate_file_path("--finetuned_weight_path", args.finetuned_weight_path)
    validate_file_path("--dataset_path", args.dataset_path)
    validate_file_path("--output_dir", args.output_dir)

    out_path = os.path.join(args.output_dir, "detail")
    tasks = [item.strip() for item in args.benchmarks.split(",")]
    model=getattr(Model, args.pretrained_model_name)

    # 构造输出结果文件名
    result_file_name=f"result_{model}"
    if args.finetuned_weight_path is not None:
        result_file_name += "_finetuned"
    result_file_name += ".json"
    output_file=os.path.join(args.output_dir, result_file_name)
    # 删除旧的结果
    if os.path.exists(output_file):
        os.remove(output_file)
    for task in tasks:
        # 检测benchmarks中字符串的合法性
        validate_enum_value(BenchMarkType, task)
        # 删除旧的评测结果
        task_eval_file = get_task_eval_file_name(model, args.finetuned_weight_path is not None, task)
        delete_files_with_keyword(out_path, task_eval_file)

    # 逐个benchmark进行评测
    results = {}
    for task in tasks:
        evaluator = AILabEvaluator(getattr(BenchMarkType, task),
                        model_name=getattr(Model, args.pretrained_model_name),
                        model_dir=args.pretrained_model_path,
                        dataset_dir=args.dataset_path,
                        tokenizer_dir=args.tokenizer_path,
                        lora_weight_dir=args.finetuned_weight_path,
                        output_dir=out_path,
                        cudaIdx=0)
        evaluator.evaluate()
        # 解析结果
        task_eval_file = get_task_eval_file_name(model, args.finetuned_weight_path is not None, task)
        update_result(results, out_path, task_eval_file)
    dumped = json.dumps(results, indent=2)

    with open(output_file, "w") as f:
        f.write(dumped)