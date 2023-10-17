import os
from typing import (Dict,  Union)
from datasets import (load_dataset,load_from_disk)
from datasets import inspect
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict

class HFDatasetAPI :
    def __init__(self) -> None:
        pass

    def load(dataset_name: str,) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        hf_dataset = load_dataset(dataset_name)
        return hf_dataset
        
    def load_disk(dataset:str)-> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        supported_dataset_format = {"csv","json","text","jsonl","png","jpg"}
        def load_file(dataset:str):
            dataset_name_format_spit = dataset.split('.')
            dataset_name_format = dataset_name_format_spit[-1].strip()
            if dataset_name_format not in supported_dataset_format:
                raise TypeError('dataset format should be json or csv or text')
            if dataset_name_format == "jsonl":
                dataset_name_format = "json"
            hf_dataset = load_dataset(path=dataset_name_format, data_files=dataset)
            return hf_dataset
    
        if os.path.isfile(dataset):
            return load_file(dataset)
        if os.path.isdir(dataset):
            files = os.listdir(dataset)
            dataset_files = set()
            for file in files:
                dataset_name_format_spit = file.split('.')
                dataset_name_format = dataset_name_format_spit[-1].strip()
                if dataset_name_format in supported_dataset_format:
                    dataset_files.add(file)
            if len(dataset_files) == 1:
                file_path = os.path.join(dataset, next(iter(dataset_files)))
                return load_file(file_path)
            else:
                return load_dataset(dataset)
    
    def list() -> str :
        dataset = inspect.list_datasets()
        return dataset
    
    def train_test_split(dataset : Dataset, test_size:float) :
        return dataset.train_test_split(test_size=test_size)