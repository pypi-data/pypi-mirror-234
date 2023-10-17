import random
import numpy as np
from torchvision import transforms
from transformers import CLIPTokenizer
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model

@PreProcessorRg.register((Task.text_to_image, Model.stable_diffusion_2_1))
class SDPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)
    
    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset,pc_dir:str,**kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = CLIPTokenizer.from_pretrained(
            pc_name_dir, subfolder="tokenizer"
        )
        return cls(dataset, tokenizer)
    
    def process_data(self) ->AILabDataset:
        accelerator = self._accelerator.accelerator_ins
        tokenizer =self._preprocessor
        dataset = self._dataset.to_hf_dataset()
        image_column = "image"
        caption_column = "text"
        resolution = 512
        center_crop = "store_true"
        random_flip = "store_true"

        def tokenize_captions(examples, is_train=True):
            captions = []
            for caption in examples[caption_column]:
                if isinstance(caption, str):
                    captions.append(caption)
                elif isinstance(caption, (list, np.ndarray)):
                    # take a random caption if there are multiple
                    captions.append(random.choice(caption) if is_train else caption[0])
                else:
                    raise ValueError(
                        f"Caption column `{caption_column}` should contain either strings or lists of strings."
                    )
            inputs = tokenizer(
                captions, max_length=tokenizer.model_max_length, padding="max_length", truncation=True, return_tensors="pt"
            )
            return inputs.input_ids
        
        train_transforms = transforms.Compose(
            [
                transforms.Resize(resolution, interpolation=transforms.InterpolationMode.BILINEAR),
                transforms.CenterCrop(resolution) if center_crop else transforms.RandomCrop(resolution),
                transforms.RandomHorizontalFlip() if random_flip else transforms.Lambda(lambda x: x),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5]),
            ]
        )

        def preprocess_train(examples):
            images = [image.convert("RGB") for image in examples[image_column]]
            examples["pixel_values"] = [train_transforms(image) for image in images]
            examples["input_ids"] = tokenize_captions(examples)
            return examples

        with accelerator.main_process_first():
            train_dataset = dataset["train"].with_transform(preprocess_train)
        return AILabDataset(train_dataset)