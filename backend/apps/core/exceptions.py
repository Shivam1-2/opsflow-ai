from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class APIError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "BAD_REQUEST"

    def __init__(self, code, message, status_code=None):
        self.detail = {"error": {"code": code, "message": message}}
        if status_code is not None:
            self.status_code = status_code


class InvalidStateTransitionError(APIError):
    def __init__(self, message):
        super().__init__(
            code="INVALID_STATE_TRANSITION",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


class TenantNotFoundError(APIError):
    def __init__(self, message="Resource not found."):
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(response.data, dict):
        if "error" not in response.data:
            if "detail" in response.data:
                code = "FORBIDDEN" if response.status_code == 403 else "ERROR"
                if response.status_code == 401:
                    code = "UNAUTHENTICATED"
                elif response.status_code == 404:
                    code = "NOT_FOUND"
                elif response.status_code == 400:
                    code = "VALIDATION_ERROR"
                detail = response.data["detail"]
                if isinstance(detail, list):
                    message = "; ".join(str(item) for item in detail)
                else:
                    message = str(detail)
                response.data = {"error": {"code": code, "message": message}}
    return response
