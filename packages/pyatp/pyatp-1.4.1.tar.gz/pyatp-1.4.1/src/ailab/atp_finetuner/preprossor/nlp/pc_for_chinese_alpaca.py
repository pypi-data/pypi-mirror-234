import torch
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_dataset.dataset import AILabDataset
from transformers import LlamaTokenizer
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@PreProcessorRg.register((Task.question_answering, Model.chinese_alpaca))
@PreProcessorRg.register((Task.question_answering, Model.chinese_alpaca_2))
class ChineseAlpacaPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir, legacy=False)
        if (len(tokenizer)) == 55296: #v2
            logger.info('v2 use flash-attention2')
            from ailab.utils.flashattenion import replace_llama_attn_with_flash_attn
            replace_llama_attn_with_flash_attn()
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        tokenizer_cls = cls(dataset, tokenizer)
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        dataset = self._dataset.to_hf_dataset()

        def buid_instruction_dataset(max_seq_length: int, preprocessing_num_workers = None,):
            from datasets import concatenate_datasets
            PROMPT_TEMPLATE_V1  = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n{instruction}\n\n### Response: "
            )
            PROMPT_TEMPLATE_V2 = (
                "[INST] <<SYS>>\n"
                "You are a helpful assistant. 你是一个乐于助人的助手。\n"
                "<</SYS>>\n\n{instruction} [/INST]"
            )
            if (len(tokenizer)) == 49954:
                logger.info('use v1 template')
                prompt = PROMPT_TEMPLATE_V1
            elif (len(tokenizer)) == 55296:
                logger.info('use v2 template')
                prompt = PROMPT_TEMPLATE_V2

            IGNORE_INDEX = -100

            def tokenization(examples):
                sources = []
                targets = []
                for instruction, input, output in zip(examples['instruction'],examples['input'],examples['output']):
                    if input is not None and input !="":
                        instruction = instruction+'\n'+input
                    source = prompt.format_map({'instruction':instruction})
                    target = f"{output}{tokenizer.eos_token}"

                    sources.append(source)
                    targets.append(target)

                tokenized_sources = tokenizer(sources,return_attention_mask=False)
                tokenized_targets = tokenizer(targets,return_attention_mask=False,add_special_tokens=False)

                all_input_ids = []
                all_labels = []
                for s,t in zip(tokenized_sources['input_ids'],tokenized_targets['input_ids']):
                    input_ids = torch.LongTensor(s + t)[:max_seq_length]
                    labels = torch.LongTensor([IGNORE_INDEX] * len(s) + t)[:max_seq_length]
                    assert len(input_ids) == len(labels)
                    all_input_ids.append(input_ids)
                    all_labels.append(labels)

                results = {'input_ids':all_input_ids, 'labels': all_labels}
                return results

            all_datasets = []
            tokenization_func = tokenization
            tokenized_dataset = dataset.map(
                tokenization_func,
                batched=True,
                num_proc=preprocessing_num_workers,
                remove_columns=["instruction","input","output"],
                keep_in_memory=False,
                desc="preprocessing on dataset",
            )
            processed_dataset = tokenized_dataset
            processed_dataset.set_format('torch')
            all_datasets.append(processed_dataset['train'])
            all_datasets = concatenate_datasets(all_datasets)
            return processed_dataset


        max_seq_length = self._max_source_length
        preprocessing_num_workers = 8
        tokenized_dataset = buid_instruction_dataset(max_seq_length,preprocessing_num_workers)
        return AILabDataset(tokenized_dataset)
