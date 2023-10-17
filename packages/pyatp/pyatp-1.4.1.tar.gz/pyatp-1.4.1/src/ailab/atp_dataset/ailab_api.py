import os
import giteapy

class AILabDatasetAPI :
    def __init__(self) -> None:
        pass

    def load(dataset_name:str, **kwargs) -> str:
        url = kwargs.get('url')
        username = kwargs.get('username')
        repo = kwargs.get('repo')
        token = kwargs.get('token')
        client = giteapy.Gitea(url, token)
        repo = client.get_repo(username, repo)
        """
        TODO: tmp return 
        """
        return './tmp/dataset.zip'

    def upload(local_file_path: str, dataset_name: str,**kwargs):
        url = kwargs.get('url')
        username = kwargs.get('username')
        repo = kwargs.get('repo')
        token = kwargs.get('token')
        client = giteapy.Gitea(url, token)
        repo = client.get_repo(username, repo)

        if os.path.isfile(local_file_path):
            pass
        elif os.path.isdir(local_file_path):
            pass

    
    def delete(object_name:str, dataset_name:str, **kwargs):
        url = kwargs.get('url')
        username = kwargs.get('username')
        repo = kwargs.get('repo')
        token = kwargs.get('token')
        client = giteapy.Gitea(url, token)
        repo = client.get_repo(username, repo)