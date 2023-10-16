#  Copyright (c) 2023 Roboto Technologies, Inc.

import collections.abc
from typing import Any, Optional, Union

from roboto.sentinels import NotSet, NotSetType

from ...domain.actions import (
    Action,
    ActionDelegate,
    ComputeRequirements,
    ContainerParameters,
    Invocation,
    InvocationDataSource,
    InvocationDelegate,
    InvocationSource,
)
from ...query import (
    ConditionType,
    QuerySpecification,
)
from ...serde import pydantic_jsonable_dict
from .trigger_delegate import TriggerDelegate
from .trigger_record import (
    TriggerForEachPrimitive,
    TriggerRecord,
)


class Trigger:
    __record: TriggerRecord
    __action_delegate: ActionDelegate
    __invocation_delegate: InvocationDelegate
    __trigger_delegate: TriggerDelegate

    @classmethod
    def create(
        cls,
        name: str,
        action_name: str,
        required_inputs: list[str],
        for_each: TriggerForEachPrimitive,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        trigger_delegate: TriggerDelegate,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
        condition: Optional[ConditionType] = None,
        additional_inputs: Optional[list[str]] = None,
        parameter_values: Optional[dict[str, Any]] = None,
        action_owner_id: Optional[str] = None,
        action_digest: Optional[str] = None,
    ) -> "Trigger":
        """
        Creates an executor trigger, which automatically invokes an action on every new dataset that meets
        some acceptance criteria.

        Args:
            name: A human-readable name for this trigger. Trigger names must be unique within each
                organization, though collisions are fine across different organizations.
            action_name: The name of an executor action to run.
                If an action with the specified name is not found, the trigger will not be created.
                If the action bound to this trigger is ever deleted, the trigger will be deleted along with it.
            required_inputs: A list of gitignore path patterns that describe a set of files required to
                invoke an action described by this trigger against a given dataset.
                An action will be invoked if at least one file is uploaded that matches each listed condition.
                Once invoked, this list of path patterns will also be used to determine which files from the dataset
                to make available to the action at runtime (i.e., downloaded into $INPUT_DIR).
                If you want to make the entire dataset available to the action, add a condition for "**/*" to the
                end of required_inputs.
            org_id: The ID of the organization the user is making this request on behalf of. If the user is
                only a member of one organization, this parameter will be set implicitly.
            compute_requirement_overrides: Optional overrides of the compute parameters specified by the
                action.
            container_parameter_overrides: Optional overrides of the container parameters specified by the
                action.
            action_delegate: An abstraction object for performing actions against the actions API.
            invocation_delegate: An abstraction object for performing actions against the invocations API.
            trigger_delegate: An abstraction object for performing actions against the triggers API.

        Returns:
            Trigger: A reference to a Trigger entity object which allows the user to perform additional operations
            on the newly created Trigger.
        """
        record = trigger_delegate.create_trigger(
            name=name,
            org_id=org_id,
            action_name=action_name,
            action_owner_id=action_owner_id,
            action_digest=action_digest,
            required_inputs=required_inputs,
            for_each=for_each,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
            created_by=created_by,
            condition=condition,
            additional_inputs=additional_inputs,
            parameter_values=parameter_values,
        )
        return cls(
            record=record,
            action_delegate=action_delegate,
            invocation_delegate=invocation_delegate,
            trigger_delegate=trigger_delegate,
        )

    @classmethod
    def from_name(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        trigger_delegate: TriggerDelegate,
        org_id: Optional[str] = None,
    ) -> "Trigger":
        record = trigger_delegate.get_trigger_by_primary_key(name=name, org_id=org_id)
        return cls(
            record=record,
            action_delegate=action_delegate,
            invocation_delegate=invocation_delegate,
            trigger_delegate=trigger_delegate,
        )

    @classmethod
    def query(
        cls,
        query: QuerySpecification,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        trigger_delegate: TriggerDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Trigger", None, None]:
        paginated_results = trigger_delegate.query_triggers(query, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(
                    record=record,
                    action_delegate=action_delegate,
                    invocation_delegate=invocation_delegate,
                    trigger_delegate=trigger_delegate,
                )
            if paginated_results.next_token:
                query.after = paginated_results.next_token
                paginated_results = trigger_delegate.query_triggers(
                    query, org_id=org_id
                )
            else:
                break

    def __init__(
        self,
        record: TriggerRecord,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        trigger_delegate: TriggerDelegate,
    ):
        self.__record = record
        self.__action_delegate = action_delegate
        self.__invocation_delegate = invocation_delegate
        self.__trigger_delegate = trigger_delegate

    @property
    def name(self):
        return self.__record.name

    @property
    def record(self) -> TriggerRecord:
        return self.__record

    @property
    def condition(self) -> Optional[ConditionType]:
        return self.__record.condition

    @property
    def for_each(self) -> TriggerForEachPrimitive:
        return self.__record.for_each

    @property
    def enabled(self) -> bool:
        return self.__record.enabled

    def delete(self):
        self.__trigger_delegate.delete_trigger(
            name=self.__record.name, org_id=self.__record.org_id
        )

    def update(
        self,
        action_name: Union[str, NotSetType] = NotSet,
        action_owner_id: Union[str, NotSetType] = NotSet,
        action_digest: Optional[Union[str, NotSetType]] = NotSet,
        required_inputs: Union[list[str], NotSetType] = NotSet,
        for_each: Union[TriggerForEachPrimitive, NotSetType] = NotSet,
        enabled: Union[bool, NotSetType] = NotSet,
        additional_inputs: Optional[Union[list[str], NotSetType]] = NotSet,
        parameter_values: Optional[Union[dict[str, Any], NotSetType]] = NotSet,
        compute_requirement_overrides: Optional[
            Union[ComputeRequirements, NotSetType]
        ] = NotSet,
        container_parameter_overrides: Optional[
            Union[ContainerParameters, NotSetType]
        ] = NotSet,
        condition: Optional[Union[ConditionType, NotSetType]] = NotSet,
        updated_by: Optional[str] = None,
    ) -> TriggerRecord:
        self.__record = self.__trigger_delegate.update_trigger(
            name=self.__record.name,
            org_id=self.__record.org_id,
            action_name=action_name,
            action_owner_id=action_owner_id,
            action_digest=action_digest,
            required_inputs=required_inputs,
            for_each=for_each,
            enabled=enabled,
            additional_inputs=additional_inputs,
            parameter_values=parameter_values,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
            condition=condition,
            updated_by=updated_by,
        )
        return self.__record

    def action(self) -> Action:
        return Action.from_name(
            name=self.__record.action.name,
            action_delegate=self.__action_delegate,
            invocation_delegate=self.__invocation_delegate,
            org_id=self.__record.org_id,
            digest=self.__record.action.digest,
            action_owner_id=self.__record.action.owner,
        )

    def invoke(
        self,
        data_source: InvocationDataSource,
        idempotency_id: Optional[str] = None,
        input_data_override: Optional[list[str]] = None,
    ) -> Invocation:
        return self.action().invoke(
            input_data=input_data_override or self.__record.required_inputs,
            data_source_id=data_source.data_source_id,
            data_source_type=data_source.data_source_type,
            invocation_source=InvocationSource.Trigger,
            invocation_source_id=self.__record.name,
            parameter_values=self.__record.parameter_values,
            compute_requirement_overrides=self.__record.compute_requirement_overrides,
            container_parameter_overrides=self.__record.container_parameter_overrides,
            idempotency_id=idempotency_id,
            org_id=self.__record.org_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)
