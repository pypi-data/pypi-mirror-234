
import argparse
from dataclasses import dataclass
import datetime
from enum import Enum
import json
import os
import sys
from typing import Dict, List, OrderedDict, Tuple
import numpy as np

METRICS = ["acc_norm", "acc_norm", "acc", "mc2", "acc_norm", "acc_norm", "correct_score", "acc", "acc"]
BENCH_TO_NAME = {
    "arc_challenge": "ARC",
    "hellaswag": "HellaSwag",
    "hendrycksTest": "MMLU",
    "truthfulqa_mc": "TruthfulQA",
    "Ceval-valid":"CEVAL",
    "Cmmlu":"CMMLU",
    "GaoKao-COMPOSITE_score":"GaoKao",
    "agi_eval":"AGIEVAL",
    "gsm8k":"GSM8K"
}

# Huggingface leaderboard
BENCHMARKS_HF = ["arc_challenge", "hellaswag", "hendrycksTest", "truthfulqa_mc"]

class ShowType(Enum):
    score = 'score'
    time = 'time'

@dataclass
class EvalResult:
    eval_name: str
    model_args: str
    results: dict

    def to_dict(self, showtype:ShowType):
        data_dict = {}
        data_dict["eval_name"] = self.eval_name # not a column, just a save name
        # data_dict["model_args"] = self.model_args
        average_hf_enable = True
        for benchmark in BENCH_TO_NAME.keys():
            if benchmark not in self.results.keys():
                self.results[benchmark] = None
                self.results[f"{benchmark}-t"] = None
                if benchmark in BENCHMARKS_HF:
                    average_hf_enable = False

        if showtype == ShowType.time:
            for k, v in BENCH_TO_NAME.items():
                data_dict[v] = self.results[f"{k}-t"]
            return data_dict

        hf_list = []
        data_dict["AVERAGE_HF"] = None
        for k, v in BENCH_TO_NAME.items():
            data_dict[v] = self.results[k]
            if k in BENCHMARKS_HF:
                hf_list.append(data_dict[v])

        if average_hf_enable:
            data_dict["AVERAGE_HF"] = sum(hf_list)/len(hf_list)
        return data_dict

def parse_eval_result(json_filepath: str) -> Tuple[str, list[dict]]:
    with open(json_filepath) as fp:
        data = json.load(fp)

    for mmlu_k in ["harness|hendrycksTest-abstract_algebra|5", "hendrycksTest-abstract_algebra"]:
        if mmlu_k in data["versions"] and data["versions"][mmlu_k] == 0:
            return None, [] # we skip models with the wrong version 

    config = data["config"]
    model_args = config.get("model_args", None)

    params_list = model_args.split(',') 
    model_params_dict = {}
    for param in params_list:
        key, value = param.split('=', 1)
        model_params_dict[key.strip()] = value.strip("'")

    peft_str = model_params_dict.get("peft", None)

    result_key = config.get("model_name", None)
    if peft_str is not None:
        peft_name = peft_str.split('/')[-1]
        result_key = f"{result_key}--{peft_name}"
    cost_time = config.get("cost_time", None)
    if cost_time is not None:
        cost_time = cost_time.split(".")[0]
    eval_results = []
    for benchmark, metric in zip(BENCH_TO_NAME.keys(), METRICS):
        accs = np.array([v[metric] for k, v in data["results"].items() if benchmark in k])
        if accs.size == 0:
            continue
        if benchmark == "GaoKao-COMPOSITE_score":
            total_score = np.array([v["total_score"] for k, v in data["results"].items() if benchmark in k])
            # 高考文科+理科总分(去掉重复的英语和语文)映射为百分制
            mean_acc = np.mean(accs/total_score) * 100.0 
        else:
            mean_acc = np.mean(accs) * 100.0
        mean_acc = round(mean_acc, 2)
        eval_results.append(EvalResult(
            eval_name=result_key, model_args=model_args, results={benchmark: mean_acc, f"{benchmark}-t":cost_time}
        ))
    return result_key, eval_results

def sort_files_by_created_time(files):
    # 获取每个文件元数据中的创建时间
    file_stats = [os.stat(file) for file in files]  
    create_times = [datetime.datetime.fromtimestamp(stat.st_ctime) for stat in file_stats]
    # 按创建时间进行排序
    sorted_paths = [x for _,x in sorted(zip(create_times,files))]

    return sorted_paths

def get_eval_results(dir:str) -> List[EvalResult]:
    json_filepaths = []
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            json_filepaths.append(os.path.join(dir, filename))
    json_filepaths = sort_files_by_created_time(json_filepaths)

    print("total:", len(json_filepaths))

    eval_results = {}
    for json_filepath in json_filepaths:
        result_key, results = parse_eval_result(json_filepath)
        for eval_result in results:
            if result_key in eval_results.keys():
                eval_results[result_key].results.update(eval_result.results)
                eval_results[result_key].model_args = eval_result.model_args
            else:
                eval_results[result_key] = eval_result

    eval_results = [v for v in eval_results.values()]

    return eval_results


def get_eval_results_dicts(dir:str, showtype:ShowType) -> List[Dict]:
    eval_results = get_eval_results(dir)

    return [e.to_dict(showtype) for e in eval_results]

def convert_time_to_seconds(time_str):
    try:
        hours, minutes, seconds = time_str.split(':')
        seconds = seconds.split('.')[0]
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        return total_seconds
    except ValueError:
        print("input is invalid!")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="./result")
    parser.add_argument("--t", choices=[enum.value for enum in ShowType], default=ShowType.score)
    args = parser.parse_args()
    r = get_eval_results_dicts(args.dir, ShowType(args.t))
    if ShowType(args.t) == ShowType.time:
        metric = "MMLU"
        r.sort(key=lambda x: convert_time_to_seconds(x[metric]) if x[metric] is not None else sys.maxsize)
    else:
        metric = "AVERAGE_HF"
        r.sort(key=lambda x: x[metric] if x[metric] is not None else 0, reverse=True)
    print(json.dumps(r, indent=2))