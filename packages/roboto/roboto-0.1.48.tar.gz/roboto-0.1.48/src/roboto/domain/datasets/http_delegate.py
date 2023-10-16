from typing import Any, Optional
import urllib.parse

from ...auth import Permissions
from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from ...updates import (
    MetadataChangeset,
    UpdateCondition,
)
from ..files import FileRecord
from .delegate import Credentials, DatasetDelegate
from .http_resources import (
    CreateDatasetRequest,
    UpdateDatasetRequest,
)
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class DatasetHttpDelegate(DatasetDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self, org_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> dict[str, str]:
        return roboto_headers(
            org_id=org_id,
            user_id=user_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_dataset(
        self,
        administrator: Administrator = Administrator.Roboto,
        metadata: Optional[dict[str, Any]] = None,
        storage_location: StorageLocation = StorageLocation.S3,
        tags: Optional[list[str]] = None,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
    ) -> DatasetRecord:
        """
        Create a new dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets"
        request_body = CreateDatasetRequest(
            administrator=administrator,
            metadata=metadata if metadata is not None else {},
            storage_location=storage_location,
            description=description,
            tags=tags if tags is not None else [],
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body),
                headers=self.headers(org_id, created_by),
            )

        return DatasetRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_dataset(self, record: DatasetRecord) -> None:
        """
        Delete a dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                headers=self.headers(record.org_id),
            )

    def get_dataset_by_primary_key(
        self,
        dataset_id: str,
        org_id: Optional[str] = None,
    ) -> DatasetRecord:
        """
        Get a dataset by its primary key (org_id, dataset_id)
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers(org_id))

        return DatasetRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_temporary_credentials(
        self,
        record: DatasetRecord,
        permissions: Permissions,
        caller: Optional[str] = None,
        transaction_id: Optional[str] = None,
    ) -> Credentials:
        """
        Get temporary credentials to access a dataset.
        """
        query_params = {"mode": permissions.value}
        encoded_qs = urllib.parse.urlencode(query_params)
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/credentials?{encoded_qs}"

        if transaction_id:
            url += f"&transaction_id={transaction_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, self.headers(record.org_id, caller))

        return Credentials.parse_obj(response.from_json(json_path=["data"]))

    def complete_upload(
        self, dataset_id: str, upload_id: str, org_id: Optional[str] = None
    ) -> None:
        """
        Marks an upload as 'completed', which allows the Roboto Platform to evaluate triggers for automatic action on
        incoming data. This also aides reporting on partial upload failure cases.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}/uploads/{upload_id}/complete"

        with RobotoHttpExceptionParse():
            self.__http_client.put(url=url, headers=self.headers(org_id))

    def list_files(
        self,
        dataset_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[FileRecord]:
        """
        List files associated with dataset.

        Files are associated with datasets in an eventually-consistent manner,
        so there will likely be delay between a file being uploaded and it appearing in this list.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}/files"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": str(page_token)})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers(org_id))

        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[FileRecord.parse_obj(file) for file in unmarshalled["items"]],
            next_token=unmarshalled["next_token"],
        )

    def query_datasets(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[DatasetRecord]:
        url = f"{self.__roboto_service_base_url}/v1/datasets/query"
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            res = self.__http_client.post(
                url,
                data=post_body,
                headers=self.headers(org_id),
            )

        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                DatasetRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: DatasetRecord,
        metadata_changeset: Optional[MetadataChangeset] = None,
        conditions: Optional[list[UpdateCondition]] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> DatasetRecord:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"
        payload = UpdateDatasetRequest(
            metadata_changeset=metadata_changeset,
            description=description,
            conditions=conditions,
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(payload, exclude_none=True),
                headers=self.headers(record.org_id, updated_by),
            )

        return DatasetRecord.parse_obj(response.from_json(json_path=["data"]))
