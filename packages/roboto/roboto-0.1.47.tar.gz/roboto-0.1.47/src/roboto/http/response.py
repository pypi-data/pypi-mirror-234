import base64
import enum
import json
import typing

from pydantic.generics import GenericModel

from ..logging import default_logger

logger = default_logger()

Model = typing.TypeVar("Model")


class PaginatedList(GenericModel, typing.Generic[Model]):
    """
    A list of records pulled from a paginated result set.
    It may be a subset of that result set,
    in which case `next_token` will be set and can be used to fetch the next page.
    """

    items: list[Model]
    # Opaque token that can be used to fetch the next page of results.
    next_token: typing.Optional[str] = None


class StreamedList(GenericModel, typing.Generic[Model]):
    """
    A StreamedList differs from a PaginatedList in that it represents a stream of data that is
    in process of being written to. Unlike a result set, which is finite and complete,
    a stream may be infinite, and it is unknown when or if it will complete.
    """

    items: list[Model]
    # Opaque token that can be used to fetch the next page of results.
    last_read: typing.Optional[str]
    # If True, it is known that there are more items to be fetched;
    # use `last_read` as a pagination token to fetch those additional records.
    # If False, it is not known if there are more items to be fetched.
    has_next: bool


class PaginationTokenEncoding(enum.Enum):
    Json = "json"
    Raw = "raw"


class PaginationTokenScheme(enum.Enum):
    V1 = "v1"


class PaginationToken:
    """
    A pagination token that can be treated as a truly opaque token by clients,
    with support for evolving the token format over time.
    """

    __scheme: PaginationTokenScheme
    __encoding: PaginationTokenEncoding
    __data: typing.Any

    @staticmethod
    def empty() -> "PaginationToken":
        return PaginationToken(
            PaginationTokenScheme.V1, PaginationTokenEncoding.Raw, None
        )

    @staticmethod
    def encode(data: str) -> str:
        """Base64 encode the data and strip all trailing padding ("=")."""
        return (
            base64.urlsafe_b64encode(data.encode("utf-8")).decode("utf-8").rstrip("=")
        )

    @staticmethod
    def decode(data: str) -> str:
        """Base64 decode the data, adding back any trailing padding ("=") as necessary to make data properly Base64."""
        while len(data) % 4 != 0:
            data += "="
        return base64.urlsafe_b64decode(data).decode("utf-8")

    @classmethod
    def from_token(cls, token: typing.Optional[str]) -> "PaginationToken":
        if token is None:
            return PaginationToken.empty()
        try:
            decoded = PaginationToken.decode(token)
            if not decoded.startswith(PaginationTokenScheme.V1.value):
                logger.error("Invalid pagination token scheme %s", decoded)
                raise ValueError("Invalid pagination token scheme")
            scheme, encoding, data = decoded.split(":", maxsplit=2)
            pagination_token_scheme = PaginationTokenScheme(scheme)
            pagination_token_encoding = PaginationTokenEncoding(encoding)
            return cls(
                pagination_token_scheme,
                pagination_token_encoding,
                json.loads(data)
                if pagination_token_encoding == PaginationTokenEncoding.Json
                else data,
            )
        except Exception as e:
            logger.error("Invalid pagination token", exc_info=e)
            raise ValueError("Invalid pagination token format") from None

    def __init__(
        self,
        scheme: PaginationTokenScheme,
        encoding: PaginationTokenEncoding,
        data: typing.Any,
    ):
        self.__scheme = scheme
        self.__encoding = encoding
        self.__data = data

    def __len__(self):
        return len(str(self)) if self.__data else 0

    def __str__(self):
        return self.to_token()

    @property
    def data(self) -> typing.Any:
        return self.__data

    def to_token(self) -> str:
        data = (
            json.dumps(self.__data)
            if self.__encoding == PaginationTokenEncoding.Json
            else self.__data
        )
        return PaginationToken.encode(
            f"{self.__scheme.value}:{self.__encoding.value}:{data}"
        )
