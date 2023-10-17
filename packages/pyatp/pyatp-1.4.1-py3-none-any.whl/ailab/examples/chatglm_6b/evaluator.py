from ailab.atp_evaluation.constant import Task, Model, BenchMarkType
from ailab.atp_evaluation.evaluator import AILabEvaluator

def eval_test(bt: BenchMarkType):
    if bt == BenchMarkType.ceval:
        dataset_path = "/home/eval_datasets/ceval"
    elif bt == BenchMarkType.mmlu:
        dataset_path = "/home/eval_datasets/mmlu"

    model_path = "/home/sdk_models/chatglm-6b"
    lora_weight_path = "/home/finetuned_models/my_chatglm_6b_model"
    tokenizer_path = "/home/sdk_models/chatglm-6b"
    output_dir = "/data1/cgzhang6"
    kshot = 0
    args = {
        "model_args": {
        },
        "benchmark_args": {
        },
    }
    evaluator = AILabEvaluator(bt,
                            Task.question_answering,
                            Model.chatglm_6b,
                            dataset_path,
                            kshot,
                            model_path,
                            tokenizer_path,
                            lora_weight_path,
                            **args)
    evaluator.evaluate()

if __name__ == '__main__':
    eval_test(BenchMarkType.ceval)
    # eval_test(BenchMarkType.mmlu)
