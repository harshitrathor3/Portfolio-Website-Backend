from enum import Enum



class StatusCodes(Enum):
    """
    Enum class for status codes.
    """
    # success responses
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    COMPILE_ERROR = 205
    NO_WORK_REQUIRED = 207

    # client error responses
    INVALID_OR_EXPIRED_TOKEN = 403
    WRONG_PAYLOAD_DATA = 405

    # server error responses
    INTERNAL_SERVER_ERROR = 500
    EMPTY_RESPONSE = 503
 