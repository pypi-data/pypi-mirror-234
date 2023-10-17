from ailab.atp_evaluation.constant import Task, Model, BenchMarkType
from ailab.atp_evaluation.evaluator import AILabEvaluator

def eval_test(bt: BenchMarkType):
    if bt == BenchMarkType.ceval:
        dataset_path = "/home/eval_datasets/ceval"
    elif bt == BenchMarkType.mmlu:
        dataset_path = "/home/eval_datasets/mmlu"

    model_path = "/home/sdk_models/llama-7b-hf"
    lora_weight_path = "/home/finetuned_models/my_standford_alpaca_model"
    tokenizer_path = "/home/sdk_models/llama-7b-hf"
    kshot = 5
    args = {
        "model_args": {
        },
        "benchmark_args": {
        },
    }
    evaluator = AILabEvaluator(bt,
                            Task.question_answering,
                            Model.alpaca,
                            dataset_path,
                            kshot,
                            model_path,
                            tokenizer_path,
                            lora_weight_path,
                            **args)
    evaluator.evaluate()

if __name__ == '__main__':
    # eval_test(BenchMarkType.ceval)
    eval_test(BenchMarkType.mmlu)
