import collections.abc
import datetime
from typing import Any, Optional, Union

from ...query import QuerySpecification
from ...sentinels import NotSet, NotSetType
from ...serde import pydantic_jsonable_dict
from ...updates import MetadataChangeset
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_delegate import ActionDelegate
from .action_record import (
    Accessibility,
    ActionParameter,
    ActionParameterChangeset,
    ActionRecord,
    ActionReference,
)
from .invocation import Invocation
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationSource,
)


class Action:
    __action_delegate: ActionDelegate
    __invocation_delegate: InvocationDelegate
    __record: ActionRecord

    @classmethod
    def create(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        parameters: Optional[list[ActionParameter]] = None,
        uri: Optional[str] = None,
        inherits: Optional[ActionReference] = None,
        compute_requirements: Optional[ComputeRequirements] = None,
        container_parameters: Optional[ContainerParameters] = None,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        created_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> "Action":
        record = action_delegate.create_action(
            name,
            parameters,
            uri,
            inherits,
            compute_requirements,
            container_parameters,
            description,
            metadata,
            tags,
            created_by,
            org_id,
        )
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def from_name(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
        digest: Optional[str] = None,
        action_owner_id: Optional[str] = None,
    ) -> "Action":
        record = action_delegate.get_action_by_primary_key(
            name, org_id, digest=digest, action_owner_id=action_owner_id
        )
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def query(
        cls,
        query: QuerySpecification,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        accessibility: Accessibility = Accessibility.Organization,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Action", None, None]:
        known = set(ActionRecord.__fields__.keys())
        actual = set()
        for field in query.fields():
            # Support dot notation for nested fields
            # E.g., "metadata.SoftwareVersion"
            if "." in field:
                actual.add(field.split(".")[0])
            else:
                actual.add(field)
        unknown = actual - known
        if unknown:
            plural = len(unknown) > 1
            msg = (
                "are not known attributes of Action"
                if plural
                else "is not a known attribute of Action"
            )
            raise ValueError(f"{unknown} {msg}. Known attributes: {known}")

        query_method = (
            action_delegate.query_actions_on_action_hub
            if accessibility == Accessibility.ActionHub
            else action_delegate.query_actions
        )
        paginated_results = query_method(query, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, action_delegate, invocation_delegate)
            if paginated_results.next_token:
                query.after = paginated_results.next_token
                paginated_results = query_method(query, org_id=org_id)
            else:
                break

    def __init__(
        self,
        record: ActionRecord,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
    ) -> None:
        self.__action_delegate = action_delegate
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    @property
    def accessibility(self) -> Accessibility:
        return self.__record.accessibility

    @property
    def compute_requirements(self) -> Optional[ComputeRequirements]:
        return self.__record.compute_requirements

    @property
    def container_parameters(self) -> Optional[ContainerParameters]:
        return self.__record.container_parameters

    @property
    def digest(self) -> str:
        return (
            self.__record.digest
            if self.__record.digest
            else self.__record.compute_digest()
        )

    @property
    def inherits_from(self) -> Optional[ActionReference]:
        return self.__record.inherits

    @property
    def last_modified(self) -> datetime.datetime:
        return self.__record.modified

    @property
    def name(self) -> str:
        return self.__record.name

    @property
    def org_id(self) -> str:
        return self.__record.org_id

    @property
    def parameters(self) -> list[ActionParameter]:
        return [param.copy() for param in self.__record.parameters]

    @property
    def record(self) -> ActionRecord:
        return self.__record

    @property
    def uri(self) -> Optional[str]:
        return self.__record.uri

    def set_accessibility(self, accessibility: Accessibility) -> None:
        self.__record = self.__action_delegate.set_accessibility(
            self.__record, accessibility
        )

    def delete(self) -> None:
        self.__action_delegate.delete_action(self.__record)

    def invoke(
        self,
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: Optional[str] = None,
        parameter_values: Optional[dict[str, Any]] = None,
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
        idempotency_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> Invocation:
        record = self.__invocation_delegate.create_invocation(
            action_record=self.__record,
            parameter_values=parameter_values if parameter_values else dict(),
            input_data=input_data,
            data_source_id=data_source_id,
            data_source_type=data_source_type,
            invocation_source=invocation_source,
            invocation_source_id=invocation_source_id,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
            idempotency_id=idempotency_id,
            org_id=org_id,
        )
        return Invocation(
            record,
            self.__invocation_delegate,
        )

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def update(
        self,
        compute_requirements: Union[ComputeRequirements, NotSetType] = NotSet,
        container_parameters: Union[ContainerParameters, NotSetType] = NotSet,
        description: Optional[Union[str, NotSetType]] = NotSet,
        metadata_changeset: Union[MetadataChangeset, NotSetType] = NotSet,
        parameter_changeset: Union[ActionParameterChangeset, NotSetType] = NotSet,
        uri: Union[str, NotSetType] = NotSet,
        updated_by: Optional[str] = None,  # A Roboto user_id
    ) -> None:
        updated = self.__action_delegate.update(
            self.__record,
            compute_requirements=compute_requirements,
            container_parameters=container_parameters,
            description=description,
            metadata_changeset=metadata_changeset,
            parameter_changeset=parameter_changeset,
            uri=uri,
            updated_by=updated_by,
        )
        self.__record = updated
