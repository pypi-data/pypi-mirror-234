import datetime
from typing import Any, Dict, List, Optional, TypedDict

import requests
from seaplane_framework.api.apis.tags import object_api
from seaplane_framework.api.model.bucket import Bucket

from ..configuration import Configuration, config
from ..util import unwrap
from .api_http import headers
from .api_request import get_pdk_client, provision_req, provision_token


# A little copy paste is better than a little dependency.
def _sizeof_fmt(num: float, suffix: str = "B") -> str:
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class ListObjectsMetadata(TypedDict):
    """
    Dictionary wrapping the metadata returned by the `list_objects()` endpoint.
    """

    name: str
    digest: str
    created_at: datetime.datetime
    size: str


class ObjectStorageAPI:
    """
    Class for handle Object Storage API calls.
    """

    def __init__(self, configuration: Configuration = config) -> None:
        self.url = f"{configuration.carrier_endpoint}/object"
        self.req = provision_req(configuration._token_api)
        self.req_token = provision_token(configuration._token_api)
        self.config = configuration

    def get_object_api(self, access_token: str) -> object_api.ObjectApi:
        return object_api.ObjectApi(get_pdk_client(access_token, cfg=self.config))

    def list_buckets(self) -> List[str]:
        def list_request(token: str) -> List[str]:
            api = self.get_object_api(token)
            list = []
            resp = api.list_buckets()
            for name, _ in sorted(resp.body.items()):
                list.append(name)

            return list

        return unwrap(self.req_token(lambda access_token: list_request(access_token)))

    def create_bucket(self, name: str, body: Optional[Bucket] = None) -> bool:
        if not body:
            body = {}

        def create_bucket_request(token: str) -> bool:
            api = self.get_object_api(token)
            path_params = {
                "bucket_name": name,
            }
            api.create_bucket(
                path_params=path_params,
                body=body,
            )
            return True

        return unwrap(
            self.req_token(lambda access_token: create_bucket_request(access_token)).map(
                lambda x: bool(x)
            )
        )

    def delete_bucket(self, name: str) -> bool:
        def delete_bucket_request(token: str) -> bool:
            api = self.get_object_api(token)
            path_params = {
                "bucket_name": name,
            }
            api.delete_bucket(path_params=path_params)
            return True

        return unwrap(
            self.req_token(lambda access_token: delete_bucket_request(access_token)).map(
                lambda x: bool(x)
            )
        )

    def list_objects(self, bucket_name: str, path_prefix: str) -> List[ListObjectsMetadata]:
        def list_request(token: str) -> List[ListObjectsMetadata]:
            api = self.get_object_api(token)

            path_params = {
                "bucket_name": bucket_name,
            }
            query_params = {
                "path": path_prefix,
            }
            resp = api.list_objects(
                path_params=path_params,
                query_params=query_params,
            )

            table = [
                ListObjectsMetadata(
                    name=x["name"],
                    digest=x["digest"],
                    created_at=datetime.datetime.fromtimestamp(int(x["mod_time"])),
                    size=_sizeof_fmt(int(x["size"])),
                )
                for x in resp.body
            ]

            return table

        return unwrap(self.req_token(lambda access_token: list_request(access_token)))

    def download(self, bucket_name: str, path: str) -> bytes:
        url = f"{self.url}/{bucket_name}/store"

        params: Dict[str, Any] = {}
        params["path"] = path

        return unwrap(
            self.req(
                lambda access_token: requests.get(
                    url,
                    params=params,
                    headers=headers(access_token, "application/octet-stream"),
                )
            ).map(lambda object: bytes(object))
        )

    def file_url(self, bucket_name: str, path: str) -> str:
        """
        Builds a URL usable to download the object stored at the given bucket & path.
        """
        return f"{self.url}/{bucket_name}/store?path={path}"

    def upload(self, bucket_name: str, path: str, object: bytes) -> bool:
        def upload_request(token: str) -> bool:
            api = self.get_object_api(token)

            path_params = {
                "bucket_name": bucket_name,
            }
            query_params = {
                "path": path,
            }

            api.create_object(
                path_params=path_params,
                query_params=query_params,
                body=object,
            )

            return True

        return unwrap(
            self.req_token(lambda access_token: upload_request(access_token)).map(
                lambda x: bool(x)
            )
        )

    def upload_file(self, bucket_name: str, path: str, object_path: str) -> bool:
        with open(object_path, "rb") as file:
            file_data = file.read()

        return self.upload(bucket_name, path, file_data)

    def delete(self, bucket_name: str, path: str) -> Any:
        def delete_request(token: str) -> bool:
            api = self.get_object_api(token)
            path_params = {
                "bucket_name": bucket_name,
            }
            query_params = {
                "path": path,
            }
            api.delete_object(
                path_params=path_params,
                query_params=query_params,
            )
            return True

        return unwrap(self.req_token(lambda access_token: delete_request(access_token)))
