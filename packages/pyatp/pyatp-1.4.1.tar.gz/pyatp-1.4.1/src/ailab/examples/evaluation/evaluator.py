import os
from ailab.atp_evaluation.constant import BenchMarkType, Model
from ailab.atp_evaluation.evaluator import AILabEvaluator

# 内置数据集本地路径
PUBLIC_DATASET_DIR:str = "/home/sdk_dataset/ailabsdk_dataset/evaluation"
# 自定义数据集本地路径(必须是全路径，即包含文件名)
PRIVATE_DATASET_DIR:str = "/home/sdk_dataset/ailabsdk_dataset/evaluation/private/wmt19.json"
OUTDIR:str = "./result"

def is_chinese_task(tasktype:BenchMarkType) -> bool:
    if (tasktype == BenchMarkType.ceval
        or tasktype == BenchMarkType.ceval_validation
        or tasktype == BenchMarkType.cmmlu
        or tasktype == BenchMarkType.gaokao
        or tasktype == BenchMarkType.agi_eval):
        return True
    return False

def llama_7b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    assert use_peft==False, "only test for llama_7b base model"
    lora_weight=None
    base_model="/home/sdk_models/llama-7b-hf"
    tokenizer_dir='/home/sdk_token/llama-7b-hf_tokenizer'
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.llama_7b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def stanford_alpaca_test(tasktype:BenchMarkType, use_peft:bool = True, gpu_index:int = 0):
    assert use_peft, "to test llama-7b-hf base model, please use llama_7b_test api, and set use_peft to False"
    lora_weight="/home/finetuned_models/my_standford_alpaca_model" if use_peft else None
    base_model="/home/sdk_models/llama-7b-hf"
    tokenizer_dir='/home/sdk_token/llama-7b-hf_tokenizer'
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.alpaca,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def vicuna_test(tasktype:BenchMarkType, use_peft:bool = True, gpu_index:int = 0):
    assert use_peft, "to test llama-7b-hf base model, please use llama_7b_test api, and set use_peft to False"
    lora_weight="/home/finetuned_models/my_chinese_llama_vicuna_model" if use_peft else None
    base_model="/home/sdk_models/llama-7b-hf"
    tokenizer_dir='/home/sdk_token/chinese_llama_vicuna_tokenizer'
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.vicuna,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def chinese_alpaca_test(tasktype:BenchMarkType, use_peft:bool = True, gpu_index:int = 0):
    assert use_peft, "to test llama-7b-hf base model, please use llama_7b_test api, and set use_peft to False"
    lora_weight="/home/finetuned_models/my_chinese_llama_alpaca_model" if use_peft else None
    base_model="/home/sdk_models/llama-7b-hf"
    tokenizer_dir='/home/sdk_token/chinese_llama_alpaca_tokenizer'
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.chinese_alpaca,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def chatglm_6b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_chatglm_6b_model" if use_peft else None
    base_model="/home/sdk_models/chatglm-6b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.chatglm_6b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def chatglm2_6b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_chatglm2_model" if use_peft else None
    base_model="/home/sdk_models/chatglm2_6b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.chatglm2_6b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def baichuan_7b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_baichuan_model" if use_peft else None
    base_model="/home/sdk_models/baichuan_7b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.baichuan_7b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def open_llama_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_open_llama_model" if use_peft else None
    base_model="/home/sdk_models/open_llama_7b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.open_llama,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def baichuan_13b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_baichuan13b_model" if use_peft else None
    base_model="/home/sdk_models/baichuan_13b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.baichuan_13b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def bloomz_7b1_mt_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_bloomz_model" if use_peft else None
    base_model="/home/sdk_models/bloomz_7b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.bloomz_7b1_mt,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def falcon_7b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_falcon_model" if use_peft else None
    base_model="/home/sdk_models/falcon_7b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.falcon_7b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def moss_moon_003_base_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_moss_model" if use_peft else None
    base_model="/home/sdk_models/moss-moon-003-base"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.moss_moon_003_base,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def llama2_7b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_llama2_model" if use_peft else None
    base_model="/home/sdk_models/llama2-7b-hf"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.llama2_7b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def llama2_chinese_alpaca_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_chinese_alpaca_2_model" if use_peft else None
    base_model="/home/sdk_models/chinese_llama_alpaca_2"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.chinese_alpaca_2,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def ziya_13b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_ziya_model" if use_peft else None
    base_model="/home/sdk_models/ziya_llama_13b/Ziya-LLaMA-13B"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.ziya_llama_13b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def internlm_7b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_internlm_model" if use_peft else None
    base_model="/home/sdk_models/internlm_7b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.internlm_7b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def belle_7b_2m_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_belle_model" if use_peft else None
    base_model="/home/sdk_models/belle_7b_2m"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.belle_7b_2m,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

def xverse_13b_test(tasktype:BenchMarkType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/home/finetuned_models/my_xverse_model" if use_peft else None
    base_model="/home/sdk_models/xverse_13b"
    tokenizer_dir=None
    evaluator = AILabEvaluator(tasktype,
                            model_name=Model.xverse_13b,
                            model_dir=base_model,
                            dataset_dir=PRIVATE_DATASET_DIR if tasktype == BenchMarkType.private else PUBLIC_DATASET_DIR,
                            tokenizer_dir=tokenizer_dir,
                            lora_weight_dir=lora_weight,
                            output_dir=OUTDIR,
                            use_accelerate=False,
                            cudaIdx=gpu_index)
    evaluator.evaluate()

# for test all models in A800
def task1(tasktype:BenchMarkType, idx:int = 0):
    vicuna_test(tasktype, use_peft = True, gpu_index = idx)
    baichuan_7b_test(tasktype, use_peft = True, gpu_index = idx)

def task2(tasktype:BenchMarkType, idx:int = 1):
    open_llama_test(tasktype, use_peft = False, gpu_index = idx)
    baichuan_7b_test(tasktype, use_peft = False, gpu_index = idx)

def task3(tasktype:BenchMarkType, idx:int = 2):
    chatglm_6b_test(tasktype, use_peft = True, gpu_index = idx)
    bloomz_7b1_mt_test(tasktype, use_peft = False, gpu_index = idx)
    bloomz_7b1_mt_test(tasktype, use_peft = True, gpu_index = idx)

def task4(tasktype:BenchMarkType, idx:int = 3):
    llama2_chinese_alpaca_test(tasktype, use_peft = False, gpu_index = idx)
    llama2_chinese_alpaca_test(tasktype, use_peft = True, gpu_index = idx)
    chatglm_6b_test(tasktype, use_peft = False, gpu_index = idx)
    chatglm2_6b_test(tasktype, use_peft = False, gpu_index = idx)
    chatglm2_6b_test(tasktype, use_peft = True, gpu_index = idx)

def task5(tasktype:BenchMarkType, idx:int = 4):
    ziya_13b_test(tasktype, use_peft = False, gpu_index = idx)
    # ziya_13b_test(tasktype, use_peft = True, gpu_index = idx)
    falcon_7b_test(tasktype, use_peft = False, gpu_index = idx)
    falcon_7b_test(tasktype, use_peft = True, gpu_index = idx)
    open_llama_test(tasktype, use_peft = True, gpu_index = idx)

def task6(tasktype:BenchMarkType, idx:int = 5):
    belle_7b_2m_test(tasktype, use_peft = False, gpu_index = idx)
    belle_7b_2m_test(tasktype, use_peft = True, gpu_index = idx)
    llama_7b_test(tasktype, use_peft = False, gpu_index = idx)
    stanford_alpaca_test(tasktype, use_peft = True, gpu_index = idx)
    chinese_alpaca_test(tasktype, use_peft = True, gpu_index = idx)

def task7(tasktype:BenchMarkType, idx:int = 6):
    internlm_7b_test(tasktype, use_peft = False, gpu_index = idx)
    internlm_7b_test(tasktype, use_peft = True, gpu_index = idx)
    llama2_7b_test(tasktype, use_peft = False, gpu_index = idx)
    moss_moon_003_base_test(tasktype, use_peft = False, gpu_index = idx)
    moss_moon_003_base_test(tasktype, use_peft = True, gpu_index = idx)

def task8(tasktype:BenchMarkType, idx:int = 7):
    xverse_13b_test(tasktype, use_peft = False, gpu_index = idx)
    xverse_13b_test(tasktype, use_peft = True, gpu_index = idx)
    llama2_7b_test(tasktype, use_peft = True, gpu_index = idx)
    baichuan_13b_test(tasktype, use_peft = False, gpu_index = idx)
    baichuan_13b_test(tasktype, use_peft = True, gpu_index = idx)

if __name__ == '__main__':
    chatglm2_6b_test(BenchMarkType.truthfulqa_mc, use_peft = False, gpu_index = 0)


 

