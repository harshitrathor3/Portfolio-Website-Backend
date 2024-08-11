from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Enum_data import StatusCodes



home_router = APIRouter(prefix="/home", tags=["home"])




@home_router.get("/")
def index():
    """
    Test route
    """
    return JSONResponse({"status": "success"}, StatusCodes.CREATED.value)
