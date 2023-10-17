import os
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_dataset.dataset import AILabDataset
from transformers import models, LlamaTokenizer
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.utils.prompter import Prompter

@PreProcessorRg.register((Task.question_answering, Model.alpaca))
@PreProcessorRg.register((Task.question_answering, Model.bencao_llama))
class AlpacaPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir, legacy=False)
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        tokenizer_cls = cls(dataset, tokenizer)
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        tokenizer.pad_token_id = (0)
        tokenizer.padding_side = "left"  # Allow batched inference

        def tokenize(prompt, add_eos_token=True):
            cutoff_len: int = self._max_source_length 

            # there's probably a way to do this with the tokenizer settings
            # but again, gotta move fast
            result = tokenizer(
                prompt,
                truncation=True,
                max_length=cutoff_len,
                padding=False,
                return_tensors=None,
            )
            if (
                result["input_ids"][-1] != tokenizer.eos_token_id
                and len(result["input_ids"]) < cutoff_len
                and add_eos_token
            ):
                result["input_ids"].append(tokenizer.eos_token_id)
                result["attention_mask"].append(1)

            result["labels"] = result["input_ids"].copy()

            return result

        def generate_and_tokenize_prompt(data_point):
            prompt_template_name: str = "alpaca"
            prompter = Prompter(prompt_template_name)
            train_on_inputs: bool = True
            add_eos_token: bool = False

            full_prompt = prompter.generate_prompt(
                data_point["instruction"],
                data_point["input"],
                data_point["output"],
            )
            tokenized_full_prompt = tokenize(full_prompt)
            if not train_on_inputs:
                user_prompt = prompter.generate_prompt(
                    data_point["instruction"], data_point["input"]
                )
                tokenized_user_prompt = tokenize(
                    user_prompt, add_eos_token=add_eos_token
                )
                user_prompt_len = len(tokenized_user_prompt["input_ids"])

                if add_eos_token:
                    user_prompt_len -= 1

                tokenized_full_prompt["labels"] = [
                    -100
                ] * user_prompt_len + tokenized_full_prompt["labels"][
                    user_prompt_len:
                ]  # could be sped up, probably
            return tokenized_full_prompt
        tokenized_dataset = self._dataset.to_hf_dataset().map(generate_and_tokenize_prompt)
        return AILabDataset(tokenized_dataset)
