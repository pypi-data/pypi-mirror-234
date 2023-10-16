import datetime
import enum
import typing
import urllib.parse

import pydantic

from ..auth import Permissions
from ..exceptions import RobotoHttpExceptionParse
from ..http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ..serde import pydantic_jsonable_dict
from ..time import utcnow
from .http_resources import (
    CreateImageRepositoryRequest,
    DeleteImageRepositoryRequest,
    DeleteImageRequest,
)
from .record import (
    ContainerImageRecord,
    ContainerImageRepositoryRecord,
)


class ContainerCredentials(pydantic.BaseModel):
    username: str
    password: str
    registry_url: str
    expiration: datetime.datetime

    def is_expired(self) -> bool:
        return utcnow() >= self.expiration

    def to_dict(self) -> dict[str, typing.Any]:
        return pydantic_jsonable_dict(self)


class RepositoryPurpose(enum.Enum):
    Executor = "executor"


class RepositoryTag(enum.Enum):
    CreatedBy = "created_by"
    OrgId = "org_id"
    Purpose = "purpose"  # RepositoryPurpose


class ImageRepository(typing.TypedDict):
    repository_name: str
    repository_uri: str


class ImageRegistry:
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def create_repository(
        self,
        repository_name: str,
        immutable_image_tags: bool = False,
        org_id: typing.Optional[str] = None,
    ) -> ImageRepository:
        """
        Create a repository for a container image in Roboto's private image registry.
        Images with different tags can be pushed to the same repository.

        Args:
            repository_name: The name of the repository to create.
            immutable_image_tags: Whether to allow image tags to be overwritten. If set to True,
                then any attempt to overwrite an existing image tag will error.

        Returns:
            A dictionary contains the `repository_name` and `repository_uri` of the created repository.
        """
        url = f"{self.__roboto_service_base_url}/v1/images/repository"
        request_body = CreateImageRepositoryRequest(
            repository_name=repository_name,
            immutable_image_tags=immutable_image_tags,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(
                    request_body, exclude_none=True, exclude_unset=True
                ),
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        return response.from_json(json_path=["data"])

    def delete_image(self, image_uri: str, org_id: typing.Optional[str] = None) -> None:
        """
        Delete a container image from Roboto's private registry.

        Args:
            image_uri: The full URI of the image to delete.
            org_id: ID of organization owning the provided image.
        """
        url = f"{self.__roboto_service_base_url}/v1/images/image"
        request_body = DeleteImageRequest(
            image_uri=image_uri,
        )

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                data=pydantic_jsonable_dict(request_body),
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

    def delete_repository(
        self,
        repository_name: str,
        org_id: typing.Optional[str] = None,
        force: bool = False,
    ) -> None:
        """
        Delete a container image from Roboto's private registry.

        Args:
            repository_name: The name of the repository to delete.
            org_id: ID of organization owning the provided image.
            force: Delete all images in the repository before deleting the repository if the repository is not empty.
        """
        url = f"{self.__roboto_service_base_url}/v1/images/repository"

        payload = DeleteImageRepositoryRequest(
            repository_name=repository_name,
            force=force,
        )

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                data=pydantic_jsonable_dict(payload),
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

    def get_container_image_record(
        self, org_id: str, image_uri: str
    ) -> ContainerImageRecord:
        url_safe_image_uri = urllib.parse.quote_plus(image_uri)
        url = f"{self.__roboto_service_base_url}/v1/images/image/record/{org_id}/{url_safe_image_uri}"

        with RobotoHttpExceptionParse():
            res = self.__http_client.get(
                url,
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        return ContainerImageRecord.parse_obj(res.from_json(["data"]))

    def get_temporary_credentials(
        self,
        repository_uri: str,
        permissions: Permissions = Permissions.ReadOnly,
        org_id: typing.Optional[str] = None,
    ) -> ContainerCredentials:
        query_params = {
            "repository_uri": repository_uri,
            "permissions": permissions.value,
        }
        encoded_qs = urllib.parse.urlencode(query_params)
        url = f"{self.__roboto_service_base_url}/v1/images/credentials?{encoded_qs}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        return ContainerCredentials.parse_obj(response.from_json(json_path=["data"]))

    def list_images(
        self,
        repository_name: typing.Optional[str] = None,
        page_token: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
    ) -> PaginatedList[ContainerImageRecord]:
        url = f"{self.__roboto_service_base_url}/v1/images/image/record/list"
        qs_params = dict()
        if repository_name:
            qs_params["repository_name"] = repository_name

        if page_token:
            qs_params["page_token"] = page_token

        if qs_params:
            encoded_qs = urllib.parse.urlencode(qs_params)
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        response_data = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                ContainerImageRecord.parse_obj(item) for item in response_data["items"]
            ],
            next_token=response_data["next_token"],
        )

    def list_repositories(
        self,
        page_token: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
    ) -> PaginatedList[ContainerImageRepositoryRecord]:
        url = f"{self.__roboto_service_base_url}/v1/images/repository/record/list"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": page_token})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        response_data = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                ContainerImageRepositoryRecord.parse_obj(item)
                for item in response_data["items"]
            ],
            next_token=response_data["next_token"],
        )

    def repository_contains_image(
        self,
        repository_name: str,
        image_tag: str,
        org_id: typing.Optional[str] = None,
    ) -> bool:
        urlsafe_repository_name = urllib.parse.quote_plus(repository_name)
        urlsafe_image_tag = urllib.parse.quote_plus(image_tag)
        url = f"{self.__roboto_service_base_url}/v1/images/repository/{urlsafe_repository_name}/contains/{urlsafe_image_tag}"  # noqa: E501

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(
                    org_id, additional_headers={"Content-Type": "application/json"}
                ),
            )

        contains_image = response.from_json(json_path=["data", "contains_image"])
        return contains_image
