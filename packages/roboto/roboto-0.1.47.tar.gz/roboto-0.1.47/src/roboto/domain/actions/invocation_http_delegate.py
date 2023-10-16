from typing import Any, Optional
import urllib.parse

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    StreamedList,
    roboto_headers,
)
from ...logging import default_logger
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import ActionRecord
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_http_resources import (
    CreateInvocationRequest,
    SetLogsLocationRequest,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
    LogRecord,
    LogsLocation,
)

logger = default_logger()


class InvocationHttpDelegate(InvocationDelegate):
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

    def cancel_invocation(
        self,
        invocation_id: str,
        org_id: Optional[str] = None,
    ) -> None:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}/cancel"
        with RobotoHttpExceptionParse():
            self.__http_client.post(url, headers=self.headers(org_id))

    def create_invocation(
        self,
        action_record: ActionRecord,
        parameter_values: dict[str, Any],
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: Optional[str] = None,
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
        idempotency_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{action_record.name}/invoke?digest={action_record.digest}"

        request_body = CreateInvocationRequest(
            parameter_values=parameter_values,
            input_data=input_data,
            data_source_id=data_source_id,
            data_source_type=data_source_type,
            invocation_source=invocation_source,
            invocation_source_id=invocation_source_id,
            idempotency_id=idempotency_id,
            compute_requirement_overrides=compute_requirement_overrides,
            container_parameter_overrides=container_parameter_overrides,
        )

        user_id = (
            invocation_source_id
            if invocation_source == InvocationSource.Manual
            else None
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(
                    org_id=org_id,
                    user_id=user_id,
                    resource_owner_id=action_record.org_id,
                ),
            )

        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_by_id(
        self, invocation_id: str, org_id: Optional[str] = None
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}"
        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers(org_id))

        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_logs(
        self,
        invocation_id: str,
        page_token: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> PaginatedList[LogRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}/logs"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": page_token})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            http_response = self.__http_client.get(url, self.headers(org_id))
        data = http_response.from_json(json_path=["data"])

        return PaginatedList(
            items=[LogRecord.parse_obj(record) for record in data["items"]],
            next_token=data["next_token"],
        )

    def stream_logs(
        self,
        invocation_id: str,
        last_read: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> StreamedList[LogRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}/logs/stream"
        if last_read:
            encoded_qs = urllib.parse.urlencode({"last_read": str(last_read)})
            url = f"{url}?{encoded_qs}"

        with RobotoHttpExceptionParse():
            http_response = self.__http_client.get(url, self.headers(org_id))
        data = http_response.from_json(json_path=["data"])

        return StreamedList(
            items=[LogRecord.parse_obj(record) for record in data["items"]],
            has_next=data["has_next"],
            last_read=data["last_read"],
        )

    def set_logs_location(
        self,
        record: InvocationRecord,
        logs: LogsLocation,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/logs"
        request_body = SetLogsLocationRequest(bucket=logs.bucket, prefix=logs.prefix)

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(record.org_id, resource_owner_id=record.org_id),
            )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def update_invocation_status(
        self,
        record: InvocationRecord,
        status: InvocationStatus,
        detail: Optional[str] = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.invocation_id}/status"

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data={"status": status.value, "detail": detail},
                headers=self.headers(record.org_id, resource_owner_id=record.org_id),
            )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_invocations(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[InvocationRecord]:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/query"
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
                InvocationRecord.parse_obj(record) for record in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )
