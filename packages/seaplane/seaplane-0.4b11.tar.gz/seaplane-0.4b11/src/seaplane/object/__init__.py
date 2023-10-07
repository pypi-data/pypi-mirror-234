from typing import Any, List

from ..api.api_object_store import ListObjectsMetadata, ObjectStorageAPI
from ..configuration import config


class ObjectStorageWrapper:
    def __init__(self) -> None:
        pass

    def list_buckets(self) -> List[str]:
        api = ObjectStorageAPI(config)
        return api.list_buckets()

    def create_bucket(self, name: str) -> Any:
        api = ObjectStorageAPI(config)
        return api.create_bucket(name)

    def delete_bucket(self, name: str) -> Any:
        api = ObjectStorageAPI(config)
        return api.delete_bucket(name)

    def exists(self, bucket_name: str, path: str) -> bool:
        api = ObjectStorageAPI(config)
        return len(api.list_objects(bucket_name, path)) > 0

    def list_objects(self, bucket_name: str, path_prefix: str) -> List[ListObjectsMetadata]:
        api = ObjectStorageAPI(config)
        return api.list_objects(bucket_name, path_prefix)

    def download(self, bucket_name: str, path: str) -> bytes:
        api = ObjectStorageAPI(config)
        return api.download(bucket_name, path)

    def upload(self, bucket_name: str, path: str, object: bytes) -> Any:
        api = ObjectStorageAPI(config)
        return api.upload(bucket_name, path, object)

    def upload_file(self, bucket_name: str, path: str, object_path: str) -> Any:
        api = ObjectStorageAPI(config)
        return api.upload_file(bucket_name, path, object_path)

    def delete(self, bucket_name: str, path: str) -> Any:
        api = ObjectStorageAPI(config)
        return api.delete(bucket_name, path)
