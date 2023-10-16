from typing import Any, Optional, Union

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...logging import default_logger
from ...query import QuerySpecification
from ...sentinels import (
    NotSet,
    NotSetType,
    is_set,
)
from ...serde import pydantic_jsonable_dict
from ...updates import MetadataChangeset
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_delegate import ActionDelegate
from .action_http_resources import (
    CreateActionRequest,
    SetActionAccessibilityRequest,
    UpdateActionRequest,
)
from .action_record import (
    Accessibility,
    ActionParameter,
    ActionParameterChangeset,
    ActionRecord,
    ActionReference,
)

logger = default_logger()


class ActionHttpDelegate(ActionDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self,
        org_id: Optional[str] = None,
        user_id: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> dict[str, str]:
        return roboto_headers(
            org_id=org_id,
            user_id=user_id,
            resource_owner_id=resource_owner_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_action(
        self,
        name: str,
        parameters: Optional[list[ActionParameter]] = None,
        uri: Optional[str] = None,
        inherits: Optional[ActionReference] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        created_by: Optional[str] = None,  # A Roboto user_id
        org_id: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions"
        request_body = CreateActionRequest(
            name=name,
            parameters=parameters,
            description=description,
            uri=uri,
            inherits=inherits,
            metadata=metadata,
            tags=tags,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(org_id, created_by),
            )

        return ActionRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_action_by_primary_key(
        self,
        name: str,
        org_id: Optional[str] = None,
        digest: Optional[str] = None,
        action_owner_id: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{name}"

        if digest:
            url += f"?digest={digest}"

        with RobotoHttpExceptionParse():
            res = self.__http_client.get(
                url,
                headers=self.headers(
                    org_id=org_id,
                    resource_owner_id=action_owner_id,
                ),
            )

        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))

    def delete_action(self, record: ActionRecord) -> None:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"
        with RobotoHttpExceptionParse():
            self.__http_client.delete(url, headers=self.headers(record.org_id))

    def query_actions(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[ActionRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/query"
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
                ActionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def query_actions_on_action_hub(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[ActionRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/query/actionhub"
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
                ActionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def set_accessibility(
        self,
        record: ActionRecord,
        accessibility: Accessibility,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}/accessibility"
        request_body = SetActionAccessibilityRequest(accessibility=accessibility)

        with RobotoHttpExceptionParse():
            res = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(request_body),
                headers=self.headers(record.org_id),
            )

        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))

    def update(
        self,
        record: ActionRecord,
        compute_requirements: Union[ComputeRequirements, NotSetType] = NotSet,
        container_parameters: Union[ContainerParameters, NotSetType] = NotSet,
        description: Optional[Union[str, NotSetType]] = NotSet,
        metadata_changeset: Union[MetadataChangeset, NotSetType] = NotSet,
        parameter_changeset: Union[ActionParameterChangeset, NotSetType] = NotSet,
        uri: Union[str, NotSetType] = NotSet,
        updated_by: Optional[str] = None,
    ) -> ActionRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"

        updates: dict[str, Any] = dict()
        if is_set(compute_requirements):
            updates["compute_requirements"] = compute_requirements
        if is_set(container_parameters):
            updates["container_parameters"] = container_parameters
        if is_set(description):
            updates["description"] = description
        if is_set(metadata_changeset):
            updates["metadata_changeset"] = metadata_changeset
        if is_set(parameter_changeset):
            updates["parameter_changeset"] = parameter_changeset
        if is_set(uri):
            updates["uri"] = uri

        request_body = UpdateActionRequest.parse_obj(updates)

        with RobotoHttpExceptionParse():
            res = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_unset=True),
                headers=self.headers(record.org_id, updated_by),
            )

        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))
