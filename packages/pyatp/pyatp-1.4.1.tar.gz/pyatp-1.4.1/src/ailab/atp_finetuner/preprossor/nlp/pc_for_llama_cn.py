from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_dataset.dataset import AILabDataset
from transformers import models, LlamaTokenizer
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model

@PreProcessorRg.register((Task.question_answering, Model.vicuna))
@PreProcessorRg.register((Task.question_answering, Model.open_llama))
class VicunaPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset,pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir, add_eos_token=True)
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        tokenizer_cls = cls(dataset, tokenizer)
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        tokenizer.pad_token_id = (0)                   
        CUTOFF_LEN = self._max_source_length
        if  CUTOFF_LEN > 512:
            CUTOFF_LEN = 512

        def generate_and_tokenize_prompt(data_point):
            # This function masks out the labels for the input,
            # so that our loss is computed only on the response.
            user_prompt = (
                (
                    f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
        ### Instruction:
        {data_point["instruction"]}
        ### Input:
        {data_point["input"]}
        ### Response:
        """
                )
                if data_point["input"]
                else (
                    f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.
        ### Instruction:
        {data_point["instruction"]}
        ### Response:
        """
                )
            )
            len_user_prompt_tokens = (
                len(
                    tokenizer(
                        user_prompt,
                        truncation=True,
                        max_length=CUTOFF_LEN + 1,
                    )["input_ids"]
                )
                - 1
            )  # no eos token
            full_tokens = tokenizer(
                user_prompt + data_point["output"],
                truncation=True,
                max_length=CUTOFF_LEN + 1,
                padding="max_length",
            )["input_ids"][:-1]
            return {
                "input_ids": full_tokens,
                "labels": [-100] * len_user_prompt_tokens
                + full_tokens[len_user_prompt_tokens:],
                "attention_mask": [1] * (len(full_tokens)),
            }
        tokenized_dataset = self._dataset.to_hf_dataset().map(generate_and_tokenize_prompt)
        return AILabDataset(tokenized_dataset)
