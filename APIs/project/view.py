from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Enum_data import StatusCodes

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/")
async def fun():
    """
    Test route
    """
    return JSONResponse({"status": "yep succes"}, StatusCodes.CREATED.value)
