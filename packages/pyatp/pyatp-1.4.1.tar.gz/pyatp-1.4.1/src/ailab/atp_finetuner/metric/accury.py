import evaluate
import numpy as np
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.build import MetricRg
from ailab.atp_finetuner.constant import Task, Model

@MetricRg.register((Task.text_classification, Model.distilbert_base_uncased))
class AccuryMetric(AILabMetric):
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def evalute(eval_pred) :
        accuracy = evaluate.load("accuracy")
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=labels)
    