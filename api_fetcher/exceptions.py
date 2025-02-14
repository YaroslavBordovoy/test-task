class BaseAPIRequestError(Exception):

    def __init__(self, message=None):
        if not message:
            message = "An API error occurred."
        super().__init__(message)


class APITimeoutError(BaseAPIRequestError):

    def __init__(self, message="Response timeout exceeded."):
        super().__init__(message)


class APIConnectionError(BaseAPIRequestError):

    def __init__(self, message="Problems connecting to API occurred."):
        super().__init__(message)


class APIResponseError(BaseAPIRequestError):

    def __init__(self, status_code=None, message="An error occurred on the server side."):
        if status_code:
            message = f"Server returned error: {status_code}."
        super().__init__(message)


class APIDataError(BaseAPIRequestError):

    def __init__(self, message="API returned not json."):
        super().__init__(message)
