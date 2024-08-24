from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Enum_data import StatusCodes
from APIs.home.control import update_visit_stats


home_router = APIRouter(prefix="/home", tags=["home"])




@home_router.get("/")
def index():
    """
    Test route
    """
    return JSONResponse({"status": "success"}, StatusCodes.CREATED.value)


@home_router.post("/hit_count")
async def hit_count():
    """
    Hit count route
    """
    ans, status_code = await update_visit_stats()
    return JSONResponse(ans, status_code)

