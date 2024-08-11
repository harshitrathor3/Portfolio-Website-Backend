from dataclasses import dataclass

@dataclass
class CustomException:
    error_msg: str
    data: dict
    exception: Exception
    trace: str
    error_code: int = 0
