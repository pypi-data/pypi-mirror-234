import transformers
from transformers import AutoTokenizer, AutoConfig
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.baichuan_7b))
@PreProcessorRg.register((Task.question_answering, Model.baichuan_13b))
@PreProcessorRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@PreProcessorRg.register((Task.question_answering, Model.falcon_7b))
@PreProcessorRg.register((Task.question_answering, Model.moss_moon_003_base))
@PreProcessorRg.register((Task.question_answering, Model.llama2_7b))
@PreProcessorRg.register((Task.question_answering, Model.internlm_7b))
@PreProcessorRg.register((Task.question_answering, Model.belle_7b_2m))
@PreProcessorRg.register((Task.question_answering, Model.xverse_13b))
@PreProcessorRg.register((Task.question_answering, Model.lawgpt_llama))
@PreProcessorRg.register((Task.question_answering, Model.educhat))
class BaichuanPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        self.model_name = None
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)
        padding_dict = {
            Model.baichuan_7b : "left",
            Model.baichuan_13b : "right",
            Model.bloomz_7b1_mt : "left",
            Model.falcon_7b : "left",
            Model.moss_moon_003_base : "left",
            Model.llama2_7b : "left",
            Model.internlm_7b : "left",
            Model.belle_7b_2m : "left",
            Model.xverse_13b : "left",
            Model.lawgpt_llama : "left",
            Model.educhat : "left",
        }
        tokenizer  = AutoTokenizer.from_pretrained(pc_name_dir,use_fast=False,
                                                   padding_side=padding_dict.get(model_name),
                                                   trust_remote_code=True)
        if tokenizer.pad_token_id is None or tokenizer.pad_token_id == 64000: # 64000 for baichuan model (older version)
            tokenizer.pad_token_id = 0 # set as the <unk> token
        if "AutoTokenizer" in tokenizer.init_kwargs.get("auto_map", {}):
            tokenizer.__class__.register_for_auto_class()
        tokenizer_cls =  cls(dataset, tokenizer)
        tokenizer_cls.model_name = model_name
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

        template_dict = {
            Model.baichuan_7b : "default",
            Model.baichuan_13b : "default",
            Model.bloomz_7b1_mt : "default",
            Model.falcon_7b : "default",
            Model.moss_moon_003_base : "moss",
            Model.llama2_7b : "llama2",
            Model.internlm_7b : "default",
            Model.belle_7b_2m : "belle",
            Model.xverse_13b : "vanilla",
            Model.lawgpt_llama : "alpaca",
            Model.educhat : "edu",
        }

        from ailab.utils.template import Template
        prefix = ""
        prompt_template = Template(template_dict.get(self.model_name))

        def get_dialog(examples):
            for i in range(len(examples["prompt"])):
                if examples["prompt"][i] and examples["response"][i]:
                    query, answer = examples["prompt"][i], examples["response"][i]
                    query = query + "\n" + examples["query"][i] if examples["query"][i] else query
                    dialog = prompt_template.get_dialog(query, answer, examples["history"][i], prefix)
                    yield dialog
        
        IGNORE_INDEX = -100
        max_source_length = self._max_source_length
        max_target_length = 512
        def preprocess_supervised_dataset(examples):
            # build inputs with format `<bos> X Y <eos>` and labels with format `<ignore> ... <ignore> Y <eos>`
            # for input with history, we build multiple input-label pairs just like:
            # https://github.com/lm-sys/FastChat/blob/f17c092f64840fa6354ed52789dccb2daa793d0b/fastchat/train/train.py#L112
            model_inputs = {"input_ids": [], "labels": []}
            max_length = max_source_length + max_target_length

            for dialog in get_dialog(examples):
                input_ids, labels = [], []

                for i in range(len(dialog) // 2):
                    source_ids = tokenizer.encode(text=dialog[2*i], add_special_tokens=(i == 0))
                    target_ids = tokenizer.encode(text=dialog[2*i+1], add_special_tokens=False)

                    if len(source_ids) > max_source_length:
                        source_ids = source_ids[:max_source_length]
                    if len(target_ids) > max_target_length - 1: # eos token
                        target_ids = target_ids[:max_target_length - 1]

                    if len(input_ids) + len(source_ids) + len(target_ids) + 1 > max_length:
                        break

                    input_ids += source_ids + target_ids + [tokenizer.eos_token_id]
                    labels += [IGNORE_INDEX] * len(source_ids) + target_ids + [tokenizer.eos_token_id]

                model_inputs["input_ids"].append(input_ids)
                model_inputs["labels"].append(labels)

            return model_inputs
    
        tokenized_dataset = datasets.map(preprocess_supervised_dataset,
                                        batched=True,
                                        remove_columns=['prompt', 'query', 'response', 'history'],)
        return AILabDataset(tokenized_dataset)