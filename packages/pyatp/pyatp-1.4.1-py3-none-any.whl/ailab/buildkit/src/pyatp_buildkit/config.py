import logging

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(ch)

SUPPORTED_DISTRO_LIST = ["ubuntu1804"]
SUPPORTED_PYVERSION_LIST = ["3.9.13", "conda-3.7", "conda-3.8", "conda-3.9"]
SUPPORTED_GOLANG_LIST = ["1.17"]
SUPPORTED_CUDA_LIST = ["10.1", "10.2", "11.2", "11.6"]

# ECR_REPO = "public.ecr.aws/iflytek-open"
ECR_REPO = "iflyopensource"
INNER_REPO = "artifacts.iflytek.com/docker-private/atp"
TEMP_GEN_DIR = "/tmp/ailab_sdk_tmpdir"
Dockerfile = "Dockerfile"

SUPPORTED_TRAIN_TASKS = ['text_classification', 'chatglm_6b', "chinese_llama_vicuna", "chinese_llama_alpaca",
                         "standford_alpaca","llama2_7b","chinese_llama_alpaca_2",
                         "chatglm2_6b", "baichuan_7b", "baichuan_13b", "bloomz_7b1_mt",
                         "falcon_7b", "moss_moon_003_base", "internlm_7b", "belle_7b_2m",
                         "xverse_13b",]

SUPPORTED_TRAIN_TASKS_WRAPPER_MAP = {
    "text_classification": "ailab/inference_wrapper/huggingface/transformers/nlp/text_classification",
    "chatglm_6b":"ailab/inference_wrapper/huggingface/lora/nlp/chatglm",
    "chinese_llama_vicuna": "ailab/inference_wrapper/huggingface/lora/nlp/vicuna",
    "chinese_llama_alpaca": "ailab/inference_wrapper/huggingface/lora/nlp/chinese_alpaca",
    "standford_alpaca": "ailab/inference_wrapper/huggingface/lora/nlp/alpaca",
    'llama2_7b': "ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "chinese_llama_alpaca_2": "ailab/inference_wrapper/huggingface/lora/nlp/chinese_alpaca",
    "chatglm2_6b":"ailab/inference_wrapper/huggingface/lora/nlp/chatglm",
    "baichuan_7b":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "baichuan_13b":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "bloomz_7b1_mt":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "falcon_7b":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "moss_moon_003_base":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "internlm_7b":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "belle_7b_2m":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
    "xverse_13b":"ailab/inference_wrapper/huggingface/lora/nlp/efficient",
}