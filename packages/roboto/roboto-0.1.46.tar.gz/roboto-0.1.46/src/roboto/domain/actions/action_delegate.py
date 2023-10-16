import abc
from typing import Any, Optional, Union

from ...http import PaginatedList
from ...query import QuerySpecification
from ...sentinels import NotSet, NotSetType
from ...updates import MetadataChangeset
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import (
    Accessibility,
    ActionParameter,
    ActionParameterChangeset,
    ActionRecord,
    ActionReference,
)


class ActionDelegate(abc.ABC):
    @abc.abstractmethod
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
        raise NotImplementedError("create_action")

    @abc.abstractmethod
    def get_action_by_primary_key(
        self,
        name: str,
        org_id: Optional[str] = None,
        digest: Optional[str] = None,
        action_owner_id: Optional[str] = None,
    ) -> ActionRecord:
        raise NotImplementedError("get_action_by_primary_key")

    @abc.abstractmethod
    def delete_action(self, record: ActionRecord) -> None:
        raise NotImplementedError("delete_action")

    @abc.abstractmethod
    def query_actions(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[ActionRecord]:
        raise NotImplementedError("query_actions")

    @abc.abstractmethod
    def query_actions_on_action_hub(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[ActionRecord]:
        raise NotImplementedError("query_actions_on_action_hub")

    @abc.abstractmethod
    def set_accessibility(
        self,
        record: ActionRecord,
        accessibility: Accessibility,
    ) -> ActionRecord:
        raise NotImplementedError("set_accessibility")

    @abc.abstractmethod
    def update(
        self,
        record: ActionRecord,
        compute_requirements: Union[ComputeRequirements, NotSetType] = NotSet,
        container_parameters: Union[ContainerParameters, NotSetType] = NotSet,
        description: Optional[Union[str, NotSetType]] = NotSet,
        metadata_changeset: Union[MetadataChangeset, NotSetType] = NotSet,
        parameter_changeset: Union[ActionParameterChangeset, NotSetType] = NotSet,
        uri: Union[str, NotSetType] = NotSet,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> ActionRecord:
        raise NotImplementedError("update")
