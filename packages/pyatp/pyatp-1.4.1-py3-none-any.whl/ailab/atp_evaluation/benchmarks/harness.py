from abc import ABC
import argparse
import json
import os
import sys
from typing import Optional

from ailab.atp_evaluation.build import BenchmarkRg
from ailab.atp_evaluation.constant import BenchMarkType, Model
from ailab.log import logger
from lm_eval import tasks, evaluator, utils

class HarnessBenchmark(ABC):
    def __init__(self, benchmark_type: BenchMarkType,
                model_name: Model = None,
                model_dir: Optional[str] = None,
                dataset_dir: str = None,
                tokenizer_dir: Optional[str] = None,
                lora_weight_dir: Optional[str] = None,
                ntrain: int = None,
                output_dir: Optional[str] = ".",
                cudaIdx: int = 0,
                use_accelerate: bool = False,
                **kwargs) -> None:
        if kwargs.get('model') is None:
            kwargs['model'] = "hf-causal-experimental"
            if model_name == Model.chatglm_6b or model_name == Model.chatglm2_6b:
                kwargs['model'] = "hf-chatglm"

        # construct model_args
        if kwargs.get('model_args') is None:
            kwargs['model_args'] = f"pretrained={model_dir}"
            if (model_name == Model.llama_7b
                or model_name == Model.alpaca
                or model_name == Model.vicuna
                or model_name == Model.chinese_alpaca
                or model_name == Model.chinese_alpaca_2
                or model_name == Model.ziya_llama_13b):
                kwargs['model_args'] += f",load_in_8bit=True,dtype='float16'"
            elif (model_name == Model.chatglm_6b or model_name == Model.chatglm2_6b):
                kwargs['model_args'] += f",add_special_tokens=True,dtype='float16',trust_remote_code=True"
            elif model_name == Model.xverse_13b or model_name == Model.belle_7b_2m:
                kwargs['model_args'] += f",dtype='bfloat16',trust_remote_code=True"
            else:
                kwargs['model_args'] += f",dtype='float16',trust_remote_code=True"
            if tokenizer_dir is not None:
                kwargs['model_args'] += f",tokenizer={tokenizer_dir}"
            if use_accelerate:
                kwargs['model_args'] += f",use_accelerate=True"
            else:
                kwargs['model_args'] += f",use_accelerate=False"


            if lora_weight_dir is not None:
                kwargs['model_args'] += f",peft={lora_weight_dir}"

        if kwargs.get('tasks') is None:
            kwargs['tasks'] = benchmark_type

        if ntrain is None:
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
            elif benchmark_type == BenchMarkType.gsm8k:
                ntrain = 8
        if kwargs.get('num_fewshot') is None:
            kwargs['num_fewshot'] = ntrain
        if kwargs.get('batch_size') is None:
            kwargs['batch_size'] = 2
            if benchmark_type == BenchMarkType.truthfulqa_mc:
                kwargs['batch_size'] = 16
        if kwargs.get('no_cache') is None:
            kwargs['no_cache'] = True
        if kwargs.get('data_dir') is None:
            kwargs['data_dir'] = dataset_dir
        if kwargs.get('device') is None:
            kwargs['device'] = f"cuda:{cudaIdx}"
        if kwargs.get('output_path') is None:
            task_name = next(attr for attr, value in vars(BenchMarkType).items() if value == benchmark_type)
            outfile = f"{model_name}_{task_name}_{ntrain}s.json"
            if lora_weight_dir is not None:
                outfile = f"{model_name}_peft_{task_name}_{ntrain}s.json"
            outfile_full_path = os.path.join(output_dir, outfile)
            kwargs['output_path'] = outfile_full_path
        logger.info(kwargs)
        # set default value
        default_args = self.__default_args()
        self.__model = kwargs.get("model", default_args.model)
        self.__model_args = kwargs.get("model_args", default_args.model_args)
        self.__tasks = kwargs.get("tasks", default_args.tasks)
        self.__provide_description = kwargs.get("provide_description", default_args.provide_description)
        self.__num_fewshot = kwargs.get("num_fewshot", default_args.num_fewshot)
        self.__batch_size = kwargs.get("batch_size", default_args.batch_size)
        self.__max_batch_size = kwargs.get("max_batch_size", default_args.max_batch_size)
        self.__device = kwargs.get("device", default_args.device)
        self.__output_path = kwargs.get("output_path", default_args.output_path)
        self.__limit = kwargs.get("limit", default_args.limit)
        self.__data_sampling = kwargs.get("data_sampling", default_args.data_sampling)
        self.__no_cache = kwargs.get("no_cache", default_args.no_cache)
        self.__decontamination_ngrams_path = kwargs.get("decontamination_ngrams_path", default_args.decontamination_ngrams_path)
        self.__description_dict_path = kwargs.get("description_dict_path", default_args.description_dict_path)
        self.__check_integrity = kwargs.get("check_integrity", default_args.check_integrity)
        self.__write_out = kwargs.get("write_out", default_args.write_out)
        self.__output_base_path = kwargs.get("output_base_path", default_args.output_base_path)
        self.__data_dir = kwargs.get("data_dir", default_args.data_dir)
        self.__model_name = model_name
        assert not self.__provide_description  # not implemented

        if self.__limit:
            logger.info(
                "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
            )

        if self.__tasks is None:
            self.__task_names = tasks.ALL_TASKS
        else:
            self.__task_names = utils.pattern_match(self.__tasks.split(","), tasks.ALL_TASKS)

        logger.info(f"Selected Tasks: {self.__task_names}")

        self.__description_dict = {}
        if self.__description_dict_path:
            with open(self.__description_dict_path, "r") as f:
                self.__description_dict = json.load(f)

    def evaluate(self):
        results = evaluator.simple_evaluate(
            model=self.__model,
            model_args=self.__model_args,
            tasks=self.__task_names,
            num_fewshot=self.__num_fewshot,
            batch_size=self.__batch_size,
            max_batch_size=self.__max_batch_size,
            device=self.__device,
            no_cache=self.__no_cache,
            limit=self.__limit,
            description_dict=self.__description_dict,
            decontamination_ngrams_path=self.__decontamination_ngrams_path,
            check_integrity=self.__check_integrity,
            write_out=self.__write_out,
            output_base_path=self.__output_base_path,
            data_dir=self.__data_dir,
        )
        results["config"]["model_name"] = self.__model_name
        results = self.__aggregation_gaokao_bench(results)
        dumped = json.dumps(results, indent=2)
        logger.info(dumped)

        if self.__output_path:
            os.makedirs(os.path.dirname(self.__output_path), exist_ok=True)
            with open(self.__output_path, "w") as f:
                f.write(dumped)

        batch_sizes = ",".join(map(str, results["config"]["batch_sizes"]))
        logger.info(
            f"{self.__model} ({self.__model_args}), limit: {self.__limit}, provide_description: {self.__provide_description}, "
            f"num_fewshot: {self.__num_fewshot}, batch_size: {self.__batch_size}{f' ({batch_sizes})' if batch_sizes else ''}"
        )
        print(evaluator.make_table(results))

    def __default_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default=None)
        parser.add_argument("--model_args", default="")
        parser.add_argument("--tasks", default=None, choices=utils.MultiChoice(tasks.ALL_TASKS))
        parser.add_argument("--provide_description", action="store_true")
        parser.add_argument("--num_fewshot", type=int, default=0)
        parser.add_argument("--batch_size", type=str, default=None)
        parser.add_argument("--max_batch_size", type=int, default=None,
                            help="Maximal batch size to try with --batch_size auto")
        parser.add_argument("--device", type=str, default=None)
        parser.add_argument("--output_path", default=None)
        parser.add_argument("--limit", type=float, default=None,
                            help="Limit the number of examples per task. "
                                "If <1, limit is a percentage of the total number of examples.")
        parser.add_argument("--data_sampling", type=float, default=None)
        parser.add_argument("--no_cache", action="store_true")
        parser.add_argument("--decontamination_ngrams_path", default=None)
        parser.add_argument("--description_dict_path", default=None)
        parser.add_argument("--check_integrity", action="store_true")
        parser.add_argument("--write_out", action="store_true", default=False)
        parser.add_argument("--output_base_path", type=str, default=None)
        parser.add_argument("--data_dir", type=str, default=None)

        return parser.parse_args([])
    
    def __aggregation_gaokao_bench(self, results):
        English_total_score = 0
        Math_1_total_score = 0
        Math_2_total_score = 0
        Chinese_total_score = 0
        Physics_total_score = 0
        Chemistry_total_score = 0
        Biology_total_score = 0
        History_total_score = 0
        Geography_total_score = 0
        Politics_total_score = 0

        English_correct_score = 0
        Math_1_correct_score = 0
        Math_2_correct_score = 0
        Chinese_correct_score = 0
        Physics_correct_score = 0
        Chemistry_correct_score = 0
        Biology_correct_score = 0
        History_correct_score = 0
        Geography_correct_score = 0
        Politics_correct_score = 0

        enabled = False
        for key, value in results["results"].items():
            if "GaoKao-" not in key:
                continue
            enabled = True
            if "English" in key:
                English_correct_score += value["correct_score"]
                English_total_score += value["total_score"]

            elif "Math_I_" in key:
                Math_1_correct_score += value["correct_score"]
                Math_1_total_score += value["total_score"]
            elif "Math_II" in key:
                Math_2_correct_score += value["correct_score"]
                Math_2_total_score += value["total_score"]
            elif "Chinese" in key:
                Chinese_correct_score += value["correct_score"]
                Chinese_total_score += value["total_score"]
            elif "Physics" in key:
                Physics_correct_score += value["correct_score"]
                Physics_total_score += value["total_score"]
            elif "Chemistry" in key:
                Chemistry_correct_score += value["correct_score"]
                Chemistry_total_score += value["total_score"]
            elif "Biology" in key:
                Biology_correct_score += value["correct_score"]
                Biology_total_score += value["total_score"]
            elif "History" in key:
                History_correct_score += value["correct_score"]
                History_total_score += value["total_score"]
            elif "Geography" in key:
                Geography_correct_score += value["correct_score"]
                Geography_total_score += value["total_score"]
            elif "Political" in key:
                Politics_correct_score += value["correct_score"]
                Politics_total_score += value["total_score"]
            else:
                print("error key:"+key)
        if not enabled:
            return results

        English_total_score = English_total_score if English_total_score != 0 else sys.maxsize
        Math_1_total_score = Math_1_total_score if Math_1_total_score != 0 else sys.maxsize
        Math_2_total_score = Math_2_total_score if Math_2_total_score != 0 else sys.maxsize
        Chinese_total_score = Chinese_total_score if Chinese_total_score != 0 else sys.maxsize
        Physics_total_score = Physics_total_score if Physics_total_score != 0 else sys.maxsize
        Chemistry_total_score = Chemistry_total_score if Chemistry_total_score != 0 else sys.maxsize
        Biology_total_score = Biology_total_score if Biology_total_score != 0 else sys.maxsize
        History_total_score = History_total_score if History_total_score != 0 else sys.maxsize
        Geography_total_score = Geography_total_score if Geography_total_score != 0 else sys.maxsize
        Politics_total_score = Politics_total_score if Politics_total_score != 0 else sys.maxsize
        # count the total score
        # English: 150 points; Math_1: 150 points; Math_2: 150 points; Chinese: 150 points; Physics: 100 points; Chemistry: 100 points; Biology: 100 points; History: 100 points; Geography: 100 points; Politics: 100 points.
        GAOKAO_A_total_score = (English_correct_score/English_total_score)*150 + (Math_1_correct_score/Math_1_total_score)*150 + (Chinese_correct_score/Chinese_total_score)*150 + (Physics_correct_score/Physics_total_score)*110 + (Chemistry_correct_score/Chemistry_total_score)*100 + (Biology_correct_score/Biology_total_score)*90
        GAOKAO_B_total_score = (English_correct_score/English_total_score)*150 + (Math_2_correct_score/Math_2_total_score)*150 + (Chinese_correct_score/Chinese_total_score)*150 + (History_correct_score/History_total_score)*100 + (Geography_correct_score/Geography_total_score)*100 + (Politics_correct_score/Politics_total_score)*100
        COMPOSITE_score = (English_correct_score/English_total_score)*150 + (Math_1_correct_score/Math_1_total_score)*150 + (Math_2_correct_score/Math_2_total_score)*150 + (Chinese_correct_score/Chinese_total_score)*150 + (Physics_correct_score/Physics_total_score)*100 + (Chemistry_correct_score/Chemistry_total_score)*100 + (Biology_correct_score/Biology_total_score)*100 + (History_correct_score/History_total_score)*100 + (Geography_correct_score/Geography_total_score)*100 + (Politics_correct_score/Politics_total_score)*100
        results["results"]["GaoKao-A_total_score"] = {
            "correct_score":GAOKAO_A_total_score,
            "total_score":750
        }
        results["versions"]["GaoKao-A_total_score"] = 0
        results["results"]["GaoKao-B_total_score"] = {
            "correct_score":GAOKAO_B_total_score,
            "total_score":750
        } 
        results["versions"]["GaoKao-B_total_score"] = 0
        results["results"]["GaoKao-COMPOSITE_score"] = {
            "correct_score":COMPOSITE_score,
            "total_score":1200
        } 
        results["versions"]["GaoKao-COMPOSITE_score"] = 0
        return results
