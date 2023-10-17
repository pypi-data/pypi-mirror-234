from abc import ABC, abstractmethod
from ailab.atp_evaluation.constant import BenchMarkType
from ailab.atp_evaluation.build import BenchmarkRg
from ailab.atp_evaluation.models.base import AILabModel

class AILabBenchmark(ABC):
    def __init__(self) -> None:
        self._choices = ["A", "B", "C", "D"]

    @classmethod
    def from_project_config(cls, model: AILabModel, benchmark_type: BenchMarkType, dataset_dir: str, ntrain: int, output_dir: str, **kwargs) :
        auto_benchmark = BenchmarkRg.get_cls(benchmark_type)
        if auto_benchmark is None:
            raise TypeError(f'auto_benchmark is None')
        args = kwargs.get('benchmark_args') or {}
        return auto_benchmark(model, dataset_dir, ntrain, output_dir, **args)

    @abstractmethod
    def evaluate(self):
        pass

    def _format_subject(self, subject):
        l = subject.split("_")
        s = ""
        for entry in l:
            s += " " + entry
        return s