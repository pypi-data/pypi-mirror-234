import enum

DEFAULT_DATASET_REVISION = 'master'

class Sources(enum.Enum):
    huggingface = 'huggingface'
    ailab = 'ailab'
 
class DownloadMode(enum.Enum):
    RESUMABLE_DOWNLOAD = 'resumable_download'
    OVERWRITE_DOWNLOAD = 'overwrite_download'

class UploadMode(enum.Enum):
    APPEND_UPDATE = 'append_update'
    OVERWRITE_UPDATE = 'overwrite_update'

