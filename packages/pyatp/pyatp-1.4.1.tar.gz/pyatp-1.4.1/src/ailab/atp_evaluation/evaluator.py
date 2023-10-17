import datetime
import time
from typing import Optional
from ailab.atp_evaluation.constant import Task, Model, BenchMarkType
from ailab.atp_evaluation.models import AILabModel
from ailab.atp_evaluation.benchmarks import AILabBenchmark
from ailab.atp_evaluation.benchmarks.harness import HarnessBenchmark
from ailab.log import logger

class AILabEvaluator:
    def __init__(self, benchmark_type: BenchMarkType,
                model_name: Model = None,
                model_dir: Optional[str] = None,
                dataset_dir: str = None,
                tokenizer_dir: Optional[str] = None,
                lora_weight_dir: Optional[str] = None,
                ntrain: int = None,
                output_dir: Optional[str] = "./result",
                task: Task = Task.question_answering,
                cudaIdx: int = 0,
                use_accelerate: bool = False,
                **args):
        if (benchmark_type == BenchMarkType.ceval or
            benchmark_type == BenchMarkType.mmlu_alt):
            model = AILabModel.from_pretrained('cuda', task, model_name, model_dir, lora_weight_dir, tokenizer_dir, cudaIdx, **args)
            benchmark = AILabBenchmark.from_project_config(model, benchmark_type, dataset_dir, ntrain, output_dir, **args)
        else:
            harness_args = args.get('benchmark_args') or {}
            benchmark = HarnessBenchmark(benchmark_type, model_name, model_dir, dataset_dir, tokenizer_dir, 
                                         lora_weight_dir, ntrain, output_dir, cudaIdx, use_accelerate, **harness_args)
        self._benchmark = benchmark

    def evaluate(self):
        start_time = time.time()
        self._benchmark.evaluate()
        end_time = time.time()
        delta_time = datetime.timedelta(seconds=(end_time-start_time))
        logger.info(f"finished, cost time {str(delta_time)}")
