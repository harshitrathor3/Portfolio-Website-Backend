from dataclasses import asdict

from fastapi.responses import JSONResponse
from data_class.general import CustomException


def handle_exception(custom_exception: CustomException) -> JSONResponse:
    """
    Handles the exception and print details.

    Args:
        custom_exception (CustomException): instance of CustomException class containing parameter details
    
    Returns:
        JSONResponse: A JSON response containing data to debug function with status code
        Response Structure:
        {
            "error_msg": "developer given error message",
            "data": {"key": "developer provided key values, generally arguments and their values"},
            "exception": "name of the exception occuered",
            "traceback": "traceback to debug",
            "error_code": "error code, if required"
        }
    """
    print("################## ERROR ##################")
    print("error message", custom_exception.error_msg)
    print('Data: ', custom_exception.data)
    print('Exception: ', custom_exception.exception)
    print('Traceback: ', custom_exception.trace)
    print('Error Code: ', custom_exception.error_code)
    print("################## ERROR ##################")
    return asdict(custom_exception)
