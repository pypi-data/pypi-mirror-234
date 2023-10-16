import collections.abc
import datetime
from typing import Any, Optional

from ...exceptions import (
    RobotoInvalidStateTransitionException,
)
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    ActionProvenance,
    ExecutableProvenance,
    InvocationDataSource,
    InvocationRecord,
    InvocationStatus,
    InvocationStatusRecord,
    LogRecord,
    LogsLocation,
    SourceProvenance,
)


class Invocation:
    __invocation_delegate: InvocationDelegate
    __record: InvocationRecord

    @classmethod
    def from_id(
        cls,
        invocation_id: str,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> "Invocation":
        record = invocation_delegate.get_by_id(invocation_id, org_id)
        return cls(record, invocation_delegate)

    @classmethod
    def query(
        cls,
        query: QuerySpecification,
        invocation_delegate: InvocationDelegate,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Invocation", None, None]:
        known = set(InvocationRecord.__fields__.keys())
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
                "are not known attributes of Invocation"
                if plural
                else "is not a known attribute of Invocation"
            )
            raise ValueError(f"{unknown} {msg}. Known attributes: {known}")

        paginated_results = invocation_delegate.query_invocations(query, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, invocation_delegate)
            if paginated_results.next_token:
                query.after = paginated_results.next_token
                paginated_results = invocation_delegate.query_invocations(
                    query, org_id=org_id
                )
            else:
                break

    def __init__(
        self, record: InvocationRecord, invocation_delegate: InvocationDelegate
    ) -> None:
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    def __str__(self) -> str:
        return str(self.__record)

    @property
    def action(self) -> ActionProvenance:
        return self.__record.provenance.action

    @property
    def compute_requirements(self) -> ComputeRequirements:
        return self.__record.compute_requirements

    @property
    def container_parameters(self) -> ContainerParameters:
        return self.__record.container_parameters

    @property
    def created(self) -> datetime.datetime:
        return self.__record.created

    @property
    def current_status(self) -> InvocationStatus:
        sorted_status_records = sorted(
            self.__record.status, key=lambda s: s.status.value
        )
        return sorted_status_records[-1].status

    @property
    def data_source(self) -> InvocationDataSource:
        return self.__record.data_source

    @property
    def executable(self) -> ExecutableProvenance:
        return self.__record.provenance.executable

    @property
    def id(self) -> str:
        return self.__record.invocation_id

    @property
    def input_data(self) -> list[str]:
        return self.__record.input_data

    @property
    def org_id(self) -> str:
        return self.__record.org_id

    @property
    def parameter_values(self) -> dict[str, Any]:
        return self.__record.parameter_values

    @property
    def record(self) -> InvocationRecord:
        return self.__record

    @property
    def reached_terminal_status(self) -> bool:
        return any(
            status_record.status.is_terminal() for status_record in self.__record.status
        )

    @property
    def source(self) -> SourceProvenance:
        return self.__record.provenance.source

    @property
    def status_log(self) -> list[InvocationStatusRecord]:
        return self.__record.status

    def cancel(self) -> None:
        if self.current_status.is_terminal():
            return

        self.__invocation_delegate.cancel_invocation(self.id, self.org_id)

    def is_queued_for_scheduling(self) -> bool:
        """
        An invocation is queued for scheduling if it:
            1. its most recent status is "queued"
            3. and is not "Deadly"
        """
        if self.current_status != InvocationStatus.Queued:
            return False

        return not any(
            status_record.status == InvocationStatus.Deadly
            for status_record in self.__record.status
        )

    def get_logs(
        self, page_token: Optional[str] = None
    ) -> collections.abc.Generator[LogRecord, None, None]:
        paginated_results = self.__invocation_delegate.get_logs(
            self.id,
            page_token,
            self.org_id,
        )
        while True:
            for record in paginated_results.items:
                yield record
            if paginated_results.next_token:
                paginated_results = self.__invocation_delegate.get_logs(
                    self.id,
                    paginated_results.next_token,
                    self.org_id,
                )
            else:
                break

    def stream_logs(
        self, last_read: Optional[str] = None
    ) -> collections.abc.Generator[LogRecord, None, Optional[str]]:
        streamed_results = self.__invocation_delegate.stream_logs(
            self.id,
            last_read,
            self.org_id,
        )
        while True:
            for record in streamed_results.items:
                yield record
            if streamed_results.has_next and streamed_results.last_read:
                streamed_results = self.__invocation_delegate.stream_logs(
                    self.id,
                    streamed_results.last_read,
                    self.org_id,
                )
            else:
                break

        return streamed_results.last_read

    def set_logs_location(self, logs: LogsLocation) -> None:
        updated_record = self.__invocation_delegate.set_logs_location(
            self.__record, logs
        )
        self.__record = updated_record

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def refresh(self) -> None:
        self.__record = self.__invocation_delegate.get_by_id(self.id, self.org_id)

    def update_status(
        self, next_status: InvocationStatus, detail: Optional[str] = "None"
    ) -> None:
        if next_status == InvocationStatus.Failed:
            # Heuristic: if this is the third time the invocation has failed, it is Deadly
            num_failures = len(
                [
                    status_record
                    for status_record in self.__record.status
                    if status_record.status == InvocationStatus.Failed
                ]
            )
            if num_failures >= 2:
                next_status = InvocationStatus.Deadly

        if not self.current_status.can_transition_to(next_status):
            raise RobotoInvalidStateTransitionException(
                f"Cannot transition invocation from {self.current_status} to {next_status}"
            )

        updated_record = self.__invocation_delegate.update_invocation_status(
            self.__record, next_status, detail
        )
        self.__record = updated_record
