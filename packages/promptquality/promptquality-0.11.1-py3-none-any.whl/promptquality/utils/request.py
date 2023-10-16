from enum import Enum
from http.client import HTTPException
from typing import Any, Callable, Dict, Optional, Union
from urllib.parse import urljoin

from requests import Response


def _validate_response(response: Response) -> None:
    if not response.ok:
        msg = (
            "Something didn't go quite right. The api returned a non-ok status "
            f"code {response.status_code} with output: {response.text}"
        )
        # TODO: Better error handling.
        raise HTTPException(msg)


def make_request(
    request_method: Callable,
    base_url: str,
    endpoint: str,
    body: Optional[Dict] = None,
    data: Optional[Dict] = None,
    files: Optional[Dict] = None,
    params: Optional[Dict] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Union[int, None] = None,
) -> Any:
    response = request_method(
        urljoin(base_url, endpoint),
        json=body,
        data=data,
        files=files,
        params=params,
        headers=headers or {},
        timeout=timeout,
    )
    _validate_response(response)
    return response.json()


class HttpHeaders(str, Enum):
    accept = "accept"
    content_type = "Content-Type"
    application_json = "application/json"

    @staticmethod
    def accept_json() -> Dict[str, str]:
        return {HttpHeaders.accept: HttpHeaders.application_json}

    @staticmethod
    def content_type_json() -> Dict[str, str]:
        return {HttpHeaders.content_type: HttpHeaders.application_json}

    @staticmethod
    def json() -> Dict[str, str]:
        return {**HttpHeaders.accept_json(), **HttpHeaders.content_type_json()}
