#  Copyright (c) 2023 Roboto Technologies, Inc.

import json
import re
from typing import Any, Optional

from ..http import HttpError
from ..serde import safe_dict_drill

__ORG_MESSAGE_PATTERN = re.compile(r"did not provide a org for single-org operation.")


class RobotoDomainException(Exception):
    """
    Expected exceptions from the Roboto domain entity objects.
    """

    _message: str
    _stack_trace: list[str]

    def __init__(self, message: str, stack_trace: list[str] = [], *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self._message = message
        self._stack_trace = stack_trace

    @staticmethod
    def from_json(contents: dict[str, Any]) -> "RobotoDomainException":
        error_code = safe_dict_drill(contents, ["error", "error_code"])
        inner_message = safe_dict_drill(contents, ["error", "message"])
        kwargs: dict[str, Any] = {}
        error = safe_dict_drill(contents, ["error"])
        if error is not None:
            kwargs.update(error)
            kwargs.pop("error_code")
            kwargs.pop("message")

        if error_code is None or inner_message is None:
            raise ValueError("Need 'error_code' and 'message' available.")

        for subclass in RobotoDomainException.__subclasses__():
            if subclass.__name__ == error_code:
                return subclass(message=inner_message, **kwargs)

        raise ValueError("Unrecognized error code 'error_code'")

    @staticmethod
    def from_client_error(error: HttpError) -> "RobotoDomainException":
        message: Optional[str]

        if type(error.msg) is dict:
            # See if it's a first class RobotoException
            try:
                return RobotoDomainException.from_json(error.msg)
            except ValueError:
                pass

            # Handle JSON from non-roboto calls
            message = error.msg.get("message", json.dumps(error.msg))
        elif type(error.msg) is str:
            message = error.msg
        else:
            message = None

        if error.status is None:
            raise RobotoDomainException(error.msg)
        if error.status == 400:
            if (
                message is not None
                and "did not provide a org for single-org operation" in message
            ):
                return RobotoNoOrgProvidedException(error.msg)
            else:
                return RobotoInvalidRequestException(error.msg)
        if error.status in (401, 403):
            return RobotoUnauthorizedException(error.msg)
        if error.status == 404:
            return RobotoNotFoundException(error.msg)
        if 500 <= error.status < 600:
            return RobotoServiceException(error.msg)
        raise error

    @property
    def http_status_code(self) -> int:
        return 500

    @property
    def error_code(self) -> str:
        return self.__class__.__name__

    @property
    def message(self) -> str:
        return self._message

    @property
    def stack_trace(self) -> list[str]:
        return self._stack_trace

    @stack_trace.setter
    def stack_trace(self, stack_trace: list[str]):
        self._stack_trace = stack_trace

    def to_dict(self) -> dict[str, Any]:
        error: dict[str, Any] = {"error_code": self.error_code, "message": self.message}
        if len(self._stack_trace) > 0:
            error["stack_trace"] = self._stack_trace
        return {"error": error}

    def serialize(self) -> str:
        return json.dumps(self.to_dict())


class RobotoUnauthorizedException(RobotoDomainException):
    """
    Thrown when a user is attempting to access a resource that they do not have permission to access
    """

    @property
    def http_status_code(self) -> int:
        return 401


class RobotoNotFoundException(RobotoDomainException):
    """
    Throw when a requested resource does not exist
    """

    @property
    def http_status_code(self) -> int:
        return 404


class RobotoIllegalArgumentException(RobotoDomainException):
    """
    Thrown when request parameters are in some way invalid
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoInvalidRequestException(RobotoDomainException):
    """
    Thrown when request parameters are in some way invalid
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoInvalidStateTransitionException(RobotoDomainException):
    """
    Thrown when requesting update of state to an invalid state, or via an invalid transition path
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoNoOrgProvidedException(RobotoDomainException):
    """
    Thrown when no org is provided to an operation which requires an org.
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoConditionException(RobotoDomainException):
    """
    Thrown if there is a failed condition
    """

    @property
    def http_status_code(self) -> int:
        return 409


class RobotoConflictException(RobotoDomainException):
    """
    Thrown if there is a conflict between a resource you're creating and another existing resource
    """

    @property
    def http_status_code(self) -> int:
        return 409


class RobotoServiceException(RobotoDomainException):
    """
    Thrown when Roboto Service failed in an unexpected way
    """


class RobotoUnknownOperationException(RobotoDomainException):
    """
    Thrown if a user is attempting to perform an action unrecognized by the Roboto platform.
    """

    @property
    def http_status_code(self) -> int:
        return 404


class RobotoLimitExceededException(RobotoDomainException):
    """
    Thrown if an operation would exceed a user or org level limit.
    """

    __resource_name: str
    __current_quantity: int
    __limit_quantity: int

    def __init__(
        self,
        message: str,
        stack_trace: list[str] = [],
        *args,
        resource_name: str = "Unknown",
        current_quantity: int = 0,
        limit_quantity: int = 0,
        **kwargs,
    ):
        super().__init__(message, stack_trace, *args, **kwargs)
        self.__resource_name = resource_name
        self.__current_quantity = current_quantity
        self.__limit_quantity = limit_quantity

    @property
    def http_status_code(self) -> int:
        return 403

    @property
    def resource_name(self) -> str:
        return self.__resource_name

    @property
    def limit_quantity(self) -> int:
        return self.__limit_quantity

    @property
    def current_quantity(self) -> int:
        return self.__current_quantity

    def to_dict(self) -> dict[str, Any]:
        as_dict = super().to_dict()
        as_dict["error"]["resource_name"] = self.resource_name
        as_dict["error"]["current_quantity"] = self.current_quantity
        as_dict["error"]["limit_quantity"] = self.limit_quantity
        return as_dict


class RobotoHttpExceptionParse(object):
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        if issubclass(type(exception), HttpError):
            raise RobotoDomainException.from_client_error(error=exception)
