from ailab.atp_evaluation.constant import Task, Model, BenchMarkType
from ailab.atp_evaluation.evaluator import AILabEvaluator

def ceval_test():
    dataset_path = "/home/eval_datasets/ceval"
    model_path = "/home/sdk_models/llama-7b-hf"
    lora_weight_path = "/home/finetuned_models/my_chinese_llama_vicuna_model"
    tokenizer_path = "/home/sdk_models/llama-7b-hf"
    kshot = 5
    args = {
        "model_args": {
        },
        "benchmark_args": {
        },
    }
    evaluator = AILabEvaluator(BenchMarkType.ceval,
                            Task.question_answering,
                            Model.vicuna,
                            dataset_path,
                            kshot,
                            model_path,
                            tokenizer_path,
                            lora_weight_path,
                            **args)
    evaluator.evaluate()

if __name__ == '__main__':
    ceval_test()