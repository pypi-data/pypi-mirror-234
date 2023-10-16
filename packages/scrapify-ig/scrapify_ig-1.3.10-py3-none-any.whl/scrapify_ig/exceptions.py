from http import HTTPStatus


class BaseError(Exception):
    message: str = "Base Error"

    def __init__(self, message: str = None) -> None:
        if message:
            self.message = message
        super().__init__(self.message)


class HTTPMethodNotAllowedError(BaseError):
    message = "HTTP Method not allowed"


class URLNotAllowedError(BaseError):
    message = "Url not allowed"


class HTTPStatusError(BaseError):
    code = None
    message_format = "{code}. {message}. {description}"
    message = "HTTP Status Error"
    description = None

    def __init__(
            self,
            code: int | str = None,
            message: str = None,
            description: str = None
    ) -> None:
        if message is not None:
            self.message = message

        if code is not None:
            self.code = code

        if description is not None:
            self.description = description

        self.message = self.message_format.format(
            code=self.code,
            message=self.message,
            description=self.description
        )
        super().__init__(self.message)


class HTTPBadRequestError(HTTPStatusError):
    code = HTTPStatus.BAD_REQUEST.value
    message = HTTPStatus.BAD_REQUEST.phrase
    description = HTTPStatus.BAD_REQUEST.description


class HTTPUnauthorizedError(HTTPStatusError):
    code = HTTPStatus.UNAUTHORIZED.value
    message = HTTPStatus.UNAUTHORIZED.phrase
    description = HTTPStatus.UNAUTHORIZED.description


class HTTPNotFoundError(HTTPStatusError):
    code = HTTPStatus.NOT_FOUND.value
    message = HTTPStatus.NOT_FOUND.phrase
    description = HTTPStatus.NOT_FOUND.description


class HTTPForbiddenError(HTTPStatusError):
    code = HTTPStatus.FORBIDDEN.value
    message = HTTPStatus.FORBIDDEN.phrase
    description = HTTPStatus.FORBIDDEN.description


class HTTPInternalServerError(HTTPStatusError):
    code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
    description = HTTPStatus.INTERNAL_SERVER_ERROR.description


class HTTPUnknownServerError(HTTPStatusError):
    code = None
    message = "Unknown server error"
    description = "Failed to determine the server response code"


class APIError(BaseError):
    message = "API Error"


class NoNextPageError(APIError):
    message = "No Next Page Error"
