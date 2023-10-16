from urllib.parse import urlparse
from http import HTTPMethod, HTTPStatus
from abc import ABC, abstractmethod, ABCMeta

import requests

from . import exceptions


__all__ = [
    "APIRequest",
]


class APIRequestInterface(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_headers(self):
        return NotImplementedError("Method get_headers must be implemented")

    @abstractmethod
    def get(
            self,
            url,
            params: dict = None,
            headers: dict = None,
            proxies: dict = None
    ):
        return NotImplementedError("Method get must be implemented")

    @abstractmethod
    def post(
            self,
            url,
            data: dict = None,
            headers: dict = None,
            proxies: dict = None
    ):
        return NotImplementedError("Method post must be implemented")

    @abstractmethod
    def api_request(
            self,
            url: str,
            method: HTTPMethod,
            params: dict = None,
            data: dict = None,
            headers: dict = None,
            proxies: dict = None
    ):
        return NotImplementedError("Method api_request must be implemented")


class APIRequest(APIRequestInterface):
    """
    The class is used to send requests to the Rapid Instagrapi  Scraper API
    https://rapidapi.com/fama-official-instagram-scraper/api/instagram-scraper-api2
    """
    RAPID_API_SCHEMA = "https"
    RAPID_API_HOST = "instagram-scraper-api2.p.rapidapi.com"
    RAPID_API_V = "v1"  # api version
    RAPID_API_URL = "{schema}://{host}/{version}".format(
        schema=RAPID_API_SCHEMA,
        host=RAPID_API_HOST,
        version=RAPID_API_V
    )

    def __init__(
            self,
            token: str
    ) -> None:
        self.token = token

    def get_headers(self) -> dict:
        return {
            "X-RapidAPI-Key": self.token,
            "X-RapidAPI-Host": self.RAPID_API_HOST
        }

    @staticmethod
    def is_absolute_url(url: str) -> bool:
        return bool(urlparse(url).netloc)

    def check_api_server_status(self) -> requests.Response:
        """
        Used to verify the status of the server API. If the answer is 200, it is good.
        If the answer is not 200 will be thrown the exception with the corresponding error.
        It is recommended to call the method after creating the Client object
        """
        response: requests.Response = self.api_request(
            url="/status",
            method=HTTPMethod.GET
        )
        return self._clean_api_response_status(response)

    def api_server_is_online(self, raise_exception=True) -> bool:
        """
        Returns True if the server API is online or False if not online.
        raise_exception=True - throws the error if the 200 response from the server fails.
        raise_exception=False - returns False instead of discarding an exception even if the server response is not 200
        """
        try:
            response: requests.Response = self.check_api_server_status()
        except Exception as e:
            if raise_exception:
                raise e
            return False
        else:
            response_data = response.json()
            return response.ok and response_data.get("detail") == "All is awesome"

    def get(
            self,
            url,
            params: dict = None,
            headers: dict = None,
            proxies: dict = None
    ) -> requests.Response:
        params = params or {}
        headers = headers or self.get_headers()
        proxies = proxies or {}
        return requests.get(url=url, params=params, headers=headers, proxies=proxies)

    def post(
            self,
            url,
            data: dict = None,
            headers: dict = None,
            proxies: dict = None
    ) -> requests.Response:
        data = data or {}
        headers = headers or self.get_headers()
        proxies = proxies or {}
        return requests.post(url=url, data=data, headers=headers, proxies=proxies)

    @staticmethod
    def _clean_api_response_status(response: requests.Response) -> requests.Response:
        """
        Checks the server response code. Returns the response object (requests.Response) if the response code is 200,
        otherwise it checks the response code and discards the corresponding error.
        For example: if the answer 500 is discarded by HTTTPInternalServerError error.
        If failed to determine the code and response code is not 200 - HTTPStatusError error will be discarded
        """
        if response.ok:
            return response

        code_400 = HTTPStatus.BAD_REQUEST.value
        code_401 = HTTPStatus.UNAUTHORIZED.value
        code_403 = HTTPStatus.FORBIDDEN.value
        code_404 = HTTPStatus.NOT_FOUND.value
        code_500 = HTTPStatus.INTERNAL_SERVER_ERROR.value

        errors = {
            code_400: exceptions.HTTPBadRequestError,
            code_401: exceptions.HTTPUnauthorizedError,
            code_403: exceptions.HTTPForbiddenError,
            code_404: exceptions.HTTPNotFoundError,
            code_500: exceptions.HTTPInternalServerError
        }

        if response.status_code in errors:
            raise errors[response.status_code]()
        else:
            raise exceptions.HTTPStatusError(code=response.status_code)

    def api_request(
            self,
            url: str,
            method: HTTPMethod,
            params: dict = None,
            data: dict = None,
            headers: dict = None,
            proxies: dict = None
    ) -> requests.Response:
        """
        Use this method to send requests to the API.
        It is recommended to use this method to get all available functionality.
        """

        if self.is_absolute_url(url):
            raise exceptions.URLNotAllowedError("URL not allowed. Url can`t be absolute")

        if not url.startswith("/"):
            raise exceptions.URLNotAllowedError("URL should starts with /")

        request_url = self.RAPID_API_URL + url

        if method == HTTPMethod.GET:
            response = self.get(
                url=request_url,
                params=params,
                headers=headers,
                proxies=proxies
            )
        elif method == HTTPMethod.POST:
            response = self.post(
                url=request_url,
                data=data,
                headers=headers,
                proxies=proxies
            )
        else:
            raise exceptions.HTTPMethodNotAllowedError()

        return self._clean_api_response_status(response)
