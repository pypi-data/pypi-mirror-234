import os
from typing import (Optional, Union)
from ailab.atp_dataset.constant import (DEFAULT_DATASET_REVISION, Sources, DownloadMode, UploadMode)
from ailab.atp_dataset.huggingface_api import HFDatasetAPI
from ailab.atp_dataset.ailab_api import AILabDatasetAPI
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict
from ailab.log import logger

class AILabDataset :
    _hf_ds = None

    def __init__(self,
                 ds_instance: Union[Dataset, IterableDataset]):
        self._hf_ds = ds_instance

    @property
    def ds_instance(self):
        return self._hf_ds

    @classmethod
    def to_ailab_dataset(cls,
                      ds_ins: Union[dict, DatasetDict, Dataset, IterableDatasetDict, IterableDataset],
                      ) -> 'AILabDataset':
        if isinstance(ds_ins, Dataset) :
            return cls(ds_ins)
        elif isinstance(ds_ins, DatasetDict) :
            return cls(next(iter(ds_ins.values())))
        elif isinstance(ds_ins, IterableDatasetDict) :
            if len(ds_ins.keys()) == 1:
                return cls(next(iter(ds_ins.values())))
            return {k: cls(v) for k, v in ds_ins.items()}
        elif isinstance(ds_ins, IterableDataset) :
            return cls(ds_ins)
        elif isinstance(ds_ins, dict) :
            return cls(next(iter(ds_ins.values())))
        else :
            raise TypeError(
                f'"ds_instance" must be a hf_ds or ms_ds, but got {type(ds_ins)}'
            )
        
    def to_hf_dataset(self) -> Dataset:
        return self._hf_ds
    
    @staticmethod
    def load_dataset(dataset_name: Union[str, list],
        version: str = DEFAULT_DATASET_REVISION,
        src: Optional[Sources] = Sources.ailab,
        data_dir: Optional[str] = None,
        data_files: Optional[str] = None,
        download_mode: Optional[DownloadMode] = DownloadMode.RESUMABLE_DOWNLOAD,
        **kwargs) -> Union[dict, 'AILabDataset']:

        """
        1.判断参数的合法性
        """
        if not isinstance(dataset_name, str) and not isinstance(dataset_name, list) :
            raise TypeError(
                f'dataset_name must be `str` or `list`, but got {type(dataset_name)}'
            )
            """
            2.判断本地文件是否存在
            2.1如果文件已经存在,直接调用transformer的load dataset
            """
        dataset_name = os.path.expanduser(dataset_name)
        is_local_path = os.path.exists(dataset_name)
        if is_local_path :
            hf_set = HFDatasetAPI.load_disk(dataset_name)
            dataset_inst = AILabDataset.to_ailab_dataset(hf_set)
            return dataset_inst
            """
            2.2.2 如果来源是huggingface 调用hf的download dataset
            """
        elif src == Sources.huggingface :
            hf_set = HFDatasetAPI.load(dataset_name)
            logger.info(f'HFDatasetAPI.load hf_set:{hf_set}')
            dataset_inst = AILabDataset.to_ailab_dataset(hf_set)
            return dataset_inst
            """
            2.2.3 如果来源是ailab 调用后台的http接口
            """
        elif src == Sources.ailab :
            ailab_dataset_path = AILabDatasetAPI.load(**kwargs)
            hf_set = HFDatasetAPI.load_disk(ailab_dataset_path)
            dataset_inst = AILabDataset.to_ailab_dataset(hf_set)
            return dataset_inst
        else :
            raise TypeError('src not support')

    @staticmethod
    def upload_dataset(local_file_path: str, dataset_name: str, 
                       upload_mode: Optional[UploadMode] = UploadMode.OVERWRITE_UPDATE,**kwargs) :
        AILabDatasetAPI.upload(local_file_path=local_file_path, dataset_name=dataset_name, **kwargs)

    
    @staticmethod
    def delete_dataset(object_name:str, dataset_name:str,**kwargs) :
        AILabDatasetAPI.delete(object_name=object_name, dataset_name=dataset_name, **kwargs)

    @staticmethod
    def list_dataset(src: Sources = Sources.ailab) -> str:
        if src == Sources.huggingface:
            return HFDatasetAPI.list()
        elif src == Sources.ailab:
            return None
    
    def train_test_split(self, test_size:float):
        if not isinstance(self.ds_instance, Dataset):
            return
        dataset = self.to_hf_dataset()
        dataset = HFDatasetAPI.train_test_split(dataset, test_size)
        self._hf_ds = dataset