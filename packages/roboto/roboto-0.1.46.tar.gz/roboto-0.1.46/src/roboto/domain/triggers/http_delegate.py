#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Any, Optional, Union

from roboto.sentinels import (
    NotSet,
    NotSetType,
    is_set,
)

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...query import (
    ConditionType,
    QuerySpecification,
)
from ...serde import pydantic_jsonable_dict
from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)
from .http_resources import (
    CreateTriggerRequest,
    UpdateTriggerRequest,
)
from .trigger_delegate import TriggerDelegate
from .trigger_record import (
    TriggerForEachPrimitive,
    TriggerRecord,
)


class TriggerHttpDelegate(TriggerDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_trigger(
        self,
        name: str,
        action_name: str,
        required_inputs: list[str],
        for_each: TriggerForEachPrimitive,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,  # A Roboto user_id
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
        condition: Optional[ConditionType] = None,
        additional_inputs: Optional[list[str]] = None,
        parameter_values: Optional[dict[str, Any]] = None,
        action_owner_id: Optional[str] = None,
        action_digest: Optional[str] = None,
    ) -> TriggerRecord:
        url = self.__http_client.url("v1/triggers")
        headers = roboto_headers(
            org_id=org_id,
            user_id=created_by,
            additional_headers={"Content-Type": "application/json"},
        )

        request_body = CreateTriggerRequest(
            name=name,
            action_name=action_name,
            action_owner_id=action_owner_id,
            action_digest=action_digest,
            required_inputs=required_inputs,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
            condition=condition,
            for_each=for_each,
            additional_inputs=additional_inputs,
            parameter_values=parameter_values,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url, data=pydantic_jsonable_dict(request_body), headers=headers
            )

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> TriggerRecord:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=headers)

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_triggers(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[TriggerRecord]:
        url = self.__http_client.url("v1/triggers/query")
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=post_body,
                headers=roboto_headers(
                    org_id=org_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                TriggerRecord.parse_obj(trigger) for trigger in unmarshalled["items"]
            ],
            next_token=unmarshalled.get("next_token"),
        )

    def delete_trigger(self, name: str, org_id: str) -> None:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url, headers=headers)

    def update_trigger(
        self,
        name: str,
        org_id: str,
        updated_by: Optional[str] = None,
        action_name: Union[str, NotSetType] = NotSet,
        action_owner_id: Union[str, NotSetType] = NotSet,
        action_digest: Optional[Union[str, NotSetType]] = NotSet,
        required_inputs: Union[list[str], NotSetType] = NotSet,
        for_each: Union[TriggerForEachPrimitive, NotSetType] = NotSet,
        enabled: Union[bool, NotSetType] = NotSet,
        additional_inputs: Optional[Union[list[str], NotSetType]] = NotSet,
        compute_requirement_overrides: Optional[
            Union[ComputeRequirements, NotSetType]
        ] = NotSet,
        container_parameter_overrides: Optional[
            Union[ContainerParameters, NotSetType]
        ] = NotSet,
        condition: Optional[Union[ConditionType, NotSetType]] = NotSet,
        parameter_values: Optional[Union[dict[str, Any], NotSetType]] = NotSet,
    ) -> TriggerRecord:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = roboto_headers(org_id=org_id)
        updates = {
            "action_name": action_name,
            "action_owner_id": action_owner_id,
            "action_digest": action_digest,
            "required_inputs": required_inputs,
            "for_each": for_each,
            "enabled": enabled,
            "additional_inputs": additional_inputs,
            "compute_requirement_overrides": compute_requirement_overrides,
            "container_parameter_overrides": container_parameter_overrides,
            "condition": condition,
            "parameter_values": parameter_values,
        }
        request_body = UpdateTriggerRequest.parse_obj(
            {k: v for k, v in updates.items() if is_set(v)}
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url=url,
                headers=headers,
                data=pydantic_jsonable_dict(request_body, exclude_unset=True),
            )

        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))
