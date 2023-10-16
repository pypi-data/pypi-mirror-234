#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Any, Optional, Union

from roboto.sentinels import NotSet, NotSetType

from ...http import PaginatedList
from ...query import (
    ConditionType,
    QuerySpecification,
)
from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)
from .trigger_record import (
    TriggerForEachPrimitive,
    TriggerRecord,
)


class TriggerDelegate(abc.ABC):
    @abc.abstractmethod
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
        raise NotImplementedError("create_trigger")

    @abc.abstractmethod
    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> TriggerRecord:
        raise NotImplementedError("get_trigger_by_primary_key")

    @abc.abstractmethod
    def query_triggers(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[TriggerRecord]:
        raise NotImplementedError("query_triggers")

    @abc.abstractmethod
    def delete_trigger(self, name: str, org_id: str) -> None:
        raise NotImplementedError("delete_trigger")

    @abc.abstractmethod
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
        raise NotImplementedError("update_trigger")
