from typing import Any
from fastapi import HTTPException, status


class CustomeHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(CustomeHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(CustomeHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not Found"


class BadRequest(CustomeHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class Unauthorized(CustomeHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Authentication required"


class DuplicateRecord(CustomeHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Email or username is already taken"


class InvalidToken(CustomeHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Invalid token"

class InvalidPassword(CustomeHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Invalid Password Reset Payload or Reset Link Expired"

class InvalidVerify(CustomeHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Invalid Password Reset Payload or Reset Link Expired"