from abc import ABC, abstractmethod
from ailab.atp_finetuner.constant import Task,Model
from ailab.atp_finetuner.build import MetricRg

class AILabMetric(ABC):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_task_model(cls, task:Task, model_name:Model):
        auto_metric = MetricRg.get_cls((task, model_name))
        if auto_metric is None:
            return None
        return auto_metric()