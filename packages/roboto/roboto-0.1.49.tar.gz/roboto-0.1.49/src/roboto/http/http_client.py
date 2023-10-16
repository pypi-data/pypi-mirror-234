import http
import json
import logging
import typing
import urllib.error
import urllib.parse
import urllib.request
import urllib.response

import tenacity
import tenacity.wait

from ..logging import LOGGER_NAME
from ..serde import safe_dict_drill

logger = logging.getLogger(LOGGER_NAME)

DEFAULT_HEADERS = object()


def is_expected_to_be_transient(exc: typing.Any) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        try:
            return http.HTTPStatus(int(exc.code)) in (
                http.HTTPStatus.TOO_MANY_REQUESTS,
                http.HTTPStatus.SERVICE_UNAVAILABLE,
            )
        except ValueError:
            return False

    # Must come after the isinstance check of HTTPError,
    # which is a subclass of URLError
    if isinstance(exc, urllib.error.URLError):
        # DNS error, probably transient
        return "Temporary failure in name resolution" in str(exc.reason)

    return False


def default_retry_wait(_exc: typing.Optional[BaseException]) -> float:
    return 1.0


class HttpError(Exception):
    __http_exc: urllib.error.HTTPError
    __msg: typing.Any = None
    __status: typing.Optional[http.HTTPStatus] = None

    def __init__(self, exc: urllib.error.HTTPError) -> None:
        super().__init__()
        self.__http_exc = exc

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.msg!r}, {self.status!r})"

    def __str__(self) -> str:
        return f"{self.msg!r}"

    @property
    def status(self) -> typing.Optional[http.HTTPStatus]:
        if self.__status is None:
            try:
                self.__status = http.HTTPStatus(int(self.__http_exc.code))
            except ValueError:
                self.__status = None
        return self.__status

    @property
    def msg(self) -> typing.Any:
        if self.__msg is None:
            decoded = self.__http_exc.read().decode("utf-8")
            try:
                self.__msg = json.loads(decoded)
            except json.JSONDecodeError:
                self.__msg = decoded
        return self.__msg

    @property
    def headers(self) -> dict:
        return dict(self.__http_exc.headers.items())


class ClientError(HttpError):
    pass


class ServerError(HttpError):
    pass


class HttpResponse:
    __response: urllib.response.addinfourl

    def __init__(self, response: urllib.response.addinfourl) -> None:
        super().__init__()
        self.__response = response

    @property
    def readable_response(self) -> urllib.response.addinfourl:
        return self.__response

    @property
    def status(self) -> http.HTTPStatus:
        status_code = self.__response.status
        if status_code is None:
            raise RuntimeError("Response has no status code")
        return http.HTTPStatus(int(status_code))

    @property
    def headers(self) -> typing.Optional[dict[str, str]]:
        return dict(self.__response.headers.items())

    def from_json(self, json_path: typing.Optional[list[str]] = None) -> typing.Any:
        with self.__response:
            unmarsalled = json.loads(self.__response.read().decode("utf-8"))
            if json_path is None:
                return unmarsalled

            return safe_dict_drill(unmarsalled, json_path)

    def from_string(self):
        with self.__response:
            return self.__response.read().decode("utf-8")


RetryWaitFn = typing.Callable[[typing.Optional[BaseException]], float]


class HttpRequest:
    url: str
    method: str
    headers: dict
    retry_wait: RetryWaitFn
    data: typing.Any = None

    def __init__(
        self,
        url: str,
        method: str = "GET",
        headers: typing.Optional[dict[str, str]] = None,
        data: typing.Any = None,
        retry_wait: typing.Optional[RetryWaitFn] = None,
    ):
        self.url = url
        self.method = method
        self.headers = headers if headers is not None else {}
        self.data = data
        self.retry_wait = retry_wait if retry_wait is not None else default_retry_wait

    def __repr__(self) -> str:
        return f"HttpRequest(url={self.url}, method={self.method}, headers={self.headers}, data={self.data})"

    @property
    def body(self) -> typing.Optional[bytes]:
        if self.data is None:
            return None

        if isinstance(self.data, bytes):
            return self.data

        if isinstance(self.data, str):
            return self.data.encode("utf-8")

        return json.dumps(self.data).encode("utf-8")

    @property
    def hostname(self) -> str:
        parsed_url = urllib.parse.urlparse(self.url)
        return (
            parsed_url.hostname
            if parsed_url.hostname is not None
            else parsed_url.netloc
        )

    def append_headers(self, headers: dict[str, str]) -> None:
        self.headers.update(headers)


HttpRequestDecorator = typing.Callable[[HttpRequest], HttpRequest]


class HttpClient:
    __base_headers: dict[str, str]
    __default_auth: typing.Optional[HttpRequestDecorator]
    __default_endpoint: typing.Optional[str]

    def __init__(
        self,
        base_headers: typing.Optional[dict[str, str]] = None,
        default_endpoint: typing.Optional[str] = None,
        default_auth: typing.Optional[HttpRequestDecorator] = None,
    ):
        self.__base_headers = base_headers if base_headers is not None else {}
        self.__default_auth = default_auth
        self.__default_endpoint = default_endpoint

    def delete(
        self, url, data: typing.Any = None, headers: typing.Optional[dict] = None
    ) -> HttpResponse:
        request = HttpRequest(url=url, method="DELETE", data=data, headers=headers)
        return self.__request(request)

    def get(
        self,
        url: str,
        headers: typing.Optional[dict] = None,
        retry_wait: RetryWaitFn = default_retry_wait,
    ) -> HttpResponse:
        request = HttpRequest(
            url=url, method="GET", headers=headers, retry_wait=retry_wait
        )
        return self.__request(request)

    def post(
        self, url, data: typing.Any = None, headers: typing.Optional[dict] = None
    ) -> HttpResponse:
        request = HttpRequest(url=url, method="POST", data=data, headers=headers)
        return self.__request(request)

    def patch(
        self, url, data: typing.Any = None, headers: typing.Optional[dict] = None
    ) -> HttpResponse:
        request = HttpRequest(url=url, method="PATCH", data=data, headers=headers)
        return self.__request(request)

    def put(
        self, url, data: typing.Any = None, headers: typing.Optional[dict] = None
    ) -> HttpResponse:
        request = HttpRequest(url=url, method="PUT", data=data, headers=headers)
        return self.__request(request)

    def url(self, path: str) -> str:
        if self.__default_endpoint is None:
            raise ValueError(
                "HttpClient.url called for client with no default endpoint. Just pass the URL clear!"
            )
        return f"{self.__default_endpoint}/{path}"

    def __request(self, request_ctx: HttpRequest) -> HttpResponse:
        if self.__default_auth is not None:
            request_ctx = self.__default_auth(request_ctx)

        logger.debug("%s", request_ctx)

        headers = self.__base_headers.copy()
        if request_ctx.headers:
            headers.update(request_ctx.headers)

        try:
            for attempt in tenacity.Retrying(
                retry=tenacity.retry_if_exception(is_expected_to_be_transient),
                stop=tenacity.stop_after_attempt(3),
                reraise=True,
                wait=self._wait(request_ctx.retry_wait),
            ):
                with attempt:
                    request = urllib.request.Request(
                        request_ctx.url, method=request_ctx.method
                    )

                    req_body = request_ctx.body
                    if req_body is not None:
                        request.data = req_body

                    for key, value in headers.items():
                        request.add_header(key, value)

                    return HttpResponse(urllib.request.urlopen(request))
        except urllib.error.HTTPError as exc:
            status_code = exc.code
            if status_code > 399 and status_code < 500:
                raise ClientError(exc) from None
            elif status_code > 499:
                raise ServerError(exc) from None
            else:
                raise HttpError(exc) from None
        except Exception:
            raise

        raise RuntimeError("Unreachable")

    def _wait(self, waiter: RetryWaitFn) -> tenacity.wait.wait_base:
        class Waiter(tenacity.wait.wait_base):
            def __call__(self, retry_state: tenacity.RetryCallState) -> float:
                outcome = retry_state.outcome
                if outcome is None:
                    return waiter(None)
                return waiter(outcome.exception())

        return Waiter()
