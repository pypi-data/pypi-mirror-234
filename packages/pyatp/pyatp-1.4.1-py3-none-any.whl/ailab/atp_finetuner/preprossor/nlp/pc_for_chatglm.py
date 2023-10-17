import transformers
from transformers import AutoTokenizer
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.chatglm_6b))
@PreProcessorRg.register((Task.question_answering, Model.chatglm2_6b))
@PreProcessorRg.register((Task.question_answering, Model.code_geex_2))
@PreProcessorRg.register((Task.question_answering, Model.finGPT_chatglm2_v3))
class ChatglmPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer  = AutoTokenizer.from_pretrained(pc_name_dir,use_fast=False,padding_side="left",trust_remote_code=True)
        assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM2-6B from HuggingFace."
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        tokenizer_cls = cls(dataset, tokenizer)
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        datasets = self._dataset.to_hf_dataset()
    
        for key,dataset in datasets.items():
            dummy_data = [None] * len(dataset)
            for column_name, target_name in [
                ("instruction", "prompt"),
                ("input", "query"),
                ("output", "response"),
                ("history", "history")
            ]: # every dataset will have 4 columns same as each other
                if column_name in dataset.column_names:
                    dataset = dataset.rename_column(column_name, target_name)
                    datasets[key] = dataset
                else:
                    dataset = dataset.add_column(target_name, dummy_data)
                    datasets[key] = dataset

        prefix = ""
        IGNORE_INDEX = -100
        max_source_length = self._max_source_length
        max_target_length = 512
        def format_example(examples): # support question with a single answer or multiple answers
            for i in range(len(examples["prompt"])):
                if examples["prompt"][i] and examples["response"][i]:
                    query, answer = examples["prompt"][i], examples["response"][i]
                    query = query + examples["query"][i] if examples["query"][i] else query
                    history = examples["history"][i] if examples["history"][i] else []
                    prompt = ""
                    for j, (old_query, response) in enumerate(history):
                        prompt += "[Round {}]\n\n问：{}\n\n答：{}\n\n".format(j+1, old_query, response)
                    prompt += "[Round {}]\n\n问：{}\n\n答：".format(len(history)+1, query)
                    prompt = prefix + prompt
                    yield prompt, answer

        def preprocess_supervised_dataset(examples):
            # v1: build inputs with format `X [gMASK] <sop> Y <eop>` and labels with format `[IGNORE] ... [IGNORE] Y <eop>`
            # v2: build inputs with format `[gMASK] sop X Y </s>` and labels with format `[IGNORE] ... [IGNORE] Y </s>`
            model_inputs = {"input_ids": [], "labels": []}
            for prompt, answer in format_example(examples):
                source_ids = tokenizer.encode(text=prompt, add_special_tokens=False)
                target_ids = tokenizer.encode(text=answer, add_special_tokens=False)

                if len(source_ids) > max_source_length - 2: # gmask and sop tokens
                    source_ids = source_ids[:max_source_length - 2]
                if len(target_ids) > max_target_length - 1: # eos token
                    target_ids = target_ids[:max_target_length - 1]

                context_length = len(source_ids) + 2 # gmask and sop tokens
                input_ids = tokenizer.build_inputs_with_special_tokens(source_ids, target_ids)
                labels = [IGNORE_INDEX] * context_length + input_ids[context_length:]

                model_inputs["input_ids"].append(input_ids)
                model_inputs["labels"].append(labels)
            return model_inputs

        tokenized_dataset = datasets.map(
                preprocess_supervised_dataset,
                batched=True,
                remove_columns=['prompt', 'query', 'response', 'history'],
            )
        return AILabDataset(tokenized_dataset)