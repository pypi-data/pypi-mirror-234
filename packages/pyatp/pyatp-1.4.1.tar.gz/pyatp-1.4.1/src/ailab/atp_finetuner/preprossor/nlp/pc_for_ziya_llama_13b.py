import torch
from torch.utils.data import Dataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_dataset.dataset import AILabDataset
from transformers import LlamaTokenizer
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model


@PreProcessorRg.register((Task.question_answering, Model.ziya_llama_13b))
class Ziyallama13bPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir)
        
        # 部分tokenizer没有pad_token_id
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.unk_token_id
        # 部分tokenizer的pad_token_id与eos_token_id相同，如InternLM，会导致无法计算eos_token_id的loss。将pad_token_id设为unk_token_id
        if tokenizer.pad_token_id == tokenizer.eos_token_id and tokenizer.unk_token_id is not None:
            tokenizer.pad_token_id = tokenizer.unk_token_id
        # 如果两者相同，模型训练时不会计算eos_token_id的loss
        if tokenizer.pad_token_id == tokenizer.eos_token_id:
            raise Exception('pad_token_id should not be equal to eos_token_id')
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        tokenizer_cls = cls(dataset, tokenizer)
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        dataset = self._dataset.to_hf_dataset()

        def buid_instruction_dataset(max_seq_length: int, preprocessing_num_workers = None,):
            from datasets import concatenate_datasets
            #PROMPT_TEMPLATE = Template('ziya')
            PROMPT_TEMPLATE = (
                "<human>:{instruction}\n<bot>:"
            )
            IGNORE_INDEX = -100

            def tokenization(examples):
                sources = []
                targets = []
                prompt = PROMPT_TEMPLATE
                for instruction, input, output in zip(examples['instruction'],examples['input'],examples['output']):
                    if input is not None and input !="":
                        instruction = instruction+'\n'+input
                    
                    #source = prompt.get_dialog(instruction, output, "", "")

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
    

