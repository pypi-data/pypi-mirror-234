import typing

from web_error.error import BadRequestException, HttpException, ServerException, UnauthorisedException


# R2XX Authorization based errors
# Auth errors AXXX
# Token errors: A0XX
# IAM errors: A1XX
class UnhandledServiceApiError(HttpException):
    pass


class ServiceApiError(HttpException):
    pass


class AuthorizationRequiredError(UnauthorisedException):
    message = "Authorization token required."
    code = "A001"


class InvalidAuthorizationError(UnauthorisedException):
    message = "Authorization token invalid."
    code = "A002"


class InsufficientPermissionsError(UnauthorisedException):
    message = "Insufficient permissions."
    code = "A100"


class InvalidResourceFormatError(BadRequestException):
    code = "A102"
    message = "Resource has invalid format."


class IdentityAccessManagerError(ServerException):
    code = "A103"
    message = "Problem with Identity Access Manager."


# Service Errors CXXX
class ServiceConnectionError(HttpException):
    code = "C001"
    status = 500

    def __init__(self, message: str, debug_message: typing.Union[str, None] = None) -> None:
        super().__init__(message, debug_message, self.code, self.status)


# SXXX Signature errors
class SignatureError(UnauthorisedException):
    code = "S001"
    message = "Signature invalid."
