from transformers import ViltProcessor, ViltConfig
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model

import torch
from PIL import Image
class VQADataset(torch.utils.data.Dataset):
    """VQA (v2) dataset."""

    def __init__(self, config, questions, annotations, images, processor):
        self.questions = questions
        self.annotations = annotations
        self.processor = processor
        self.config = config
        self.images = images

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        # get image + text
        annotation = self.annotations[idx]
        image = self.images[idx]
        text = self.questions[idx]
        
        encoding = self.processor(image, text, padding="max_length", truncation=True, return_tensors="pt")
        # remove batch dimension
        for k,v in encoding.items():
          encoding[k] = v.squeeze()
        # add labels
        labels = annotation['labels']
        scores = annotation['scores']
        # based on: https://github.com/dandelin/ViLT/blob/762fd3975c180db6fc88f577cf39549983fa373a/vilt/modules/objectives.py#L301
        targets = torch.zeros(len(self.config.id2label))
        for label, score in zip(labels, scores):
              targets[label] = score
        encoding["labels"] = targets

        return encoding

@PreProcessorRg.register((Task.visual_question_answering, Model.vilt))
class ViltPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        self.config = None
        super().__init__(dataset, preprocessor)
    
    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset,pc_dir:str,**kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        config = ViltConfig.from_pretrained(pc_name_dir)
        hf_preprocessor = ViltProcessor.from_pretrained(pc_name_dir)
        vilt_ins =  cls(dataset, hf_preprocessor)
        vilt_ins.config = config
        return vilt_ins
    
    def process_data(self) ->AILabDataset:
        processor = self._preprocessor
        dataset = self._dataset.to_hf_dataset()["train"]
        answers = dataset["answers_original"]
        annotations = []
        config = self.config
        def get_score(count: int) -> float:
            return min(1.0, count / 3)

        for answer_list in answers:
            answer_count = {}
            for answer in answer_list:
                answer_ = answer["answer"]
                answer_count[answer_] = answer_count.get(answer_, 0) + 1
            labels = []
            scores = []
            for answer in answer_count:
                if answer not in list(config.label2id.keys()):
                    continue
                labels.append(config.label2id[answer])
                score = get_score(answer_count[answer])
                scores.append(score)

            annotation = {}
            annotation['labels'] = labels
            annotation['scores'] = scores
            annotations.append(annotation)

        vqadataset = VQADataset(config = self.config,
                     questions=dataset["question"][:100],
                     annotations=annotations[:100],
                     images = dataset["image"][:100],
                     processor=processor)
        return AILabDataset(vqadataset)
