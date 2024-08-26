from abc import ABC, abstractmethod
import os
from typing import Union
# from replit.object_storage import Client as ReplitClient
# from replit.object_storage.errors import ObjectNotFoundError

class StorageInterface(ABC):
    @abstractmethod
    def upload(self, file_name: str, content: bytes) -> str:
        pass

    @abstractmethod
    def download(self, file_name: str) -> Union[bytes, None]:
        pass

# class ReplitObjectStorage(StorageInterface):
#     def __init__(self):
#         self.client = ReplitClient()

#     def upload(self, file_name: str, content: bytes) -> str:
#         self.client.upload_from_bytes(file_name, content)
#         return file_name

#     def download(self, file_name: str) -> Union[bytes, None]:
#         try:
#             return self.client.download_as_bytes(file_name)
#         except ObjectNotFoundError:
#             return None

class LocalFileStorage(StorageInterface):
    def __init__(self, base_path: str = 'uploads'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def upload(self, file_name: str, content: bytes) -> str:
        file_path = os.path.join(self.base_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(content)
        return file_path

    def download(self, file_name: str) -> Union[bytes, None]:
        file_path = os.path.join(self.base_path, file_name)
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None

def get_storage() -> StorageInterface:
    # if os.environ.get('REPL_ID'):
    #     return ReplitObjectStorage()
    # else:
    return LocalFileStorage()