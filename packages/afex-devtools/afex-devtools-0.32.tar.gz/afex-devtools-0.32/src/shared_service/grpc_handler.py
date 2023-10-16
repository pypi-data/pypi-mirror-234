from rest_framework import status
from grpc import StatusCode
from google.protobuf.json_format import MessageToDict
from any_case import converts_keys
import json

class gRPCHandler:
    def __init__(self):
        self.error_map = {
            StatusCode.OK: status.HTTP_200_OK,
            StatusCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
            StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
            StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
            StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
            StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
            StatusCode.ABORTED: status.HTTP_410_GONE,
            StatusCode.RESOURCE_EXHAUSTED: status.HTTP_429_TOO_MANY_REQUESTS,
            StatusCode.INTERNAL: status.HTTP_500_INTERNAL_SERVER_ERROR,
            StatusCode.UNIMPLEMENTED: status.HTTP_501_NOT_IMPLEMENTED,
            StatusCode.UNKNOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,
            StatusCode.UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
            StatusCode.DEADLINE_EXCEEDED: status.HTTP_504_GATEWAY_TIMEOUT,
            StatusCode.OUT_OF_RANGE: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            StatusCode.CANCELLED: status.HTTP_405_METHOD_NOT_ALLOWED,
            StatusCode.FAILED_PRECONDITION: status.HTTP_412_PRECONDITION_FAILED,
            StatusCode.DATA_LOSS: status.HTTP_422_UNPROCESSABLE_ENTITY
        }

    def grpc_call(self, call, message, metadata=None):
        try:
            data = call(message, metadata=metadata)
            ret_data = MessageToDict(data, including_default_value_fields=True)
            ret_data = converts_keys(ret_data, case='snake')
            return ret_data, None
        except Exception as e:
            return None, self.grpc_error(e)

    def grpc_error(self, e):
        try:
            code = e.code()
        except:
            code = StatusCode.UNKNOWN

        try:
            d = e.details()
        except:
            d = str(e)

        try:
            details = json.loads(d)
        except:
            details = d

        return {
            "error": details,
            "status_code": self.error_map[code]
        }
