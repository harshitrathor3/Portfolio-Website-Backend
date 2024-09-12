from fastapi.responses import JSONResponse
from fastapi import APIRouter, Form, File, UploadFile

from Enum_data import StatusCodes
from APIs.home.payload_structure import TestimonialFormat
from APIs.home.control import update_visit_stats, fetch_testimonials, add_single_testimonial

home_router = APIRouter(prefix="/home", tags=["home"])

# TODO add try except in all routes


@home_router.get("/")
def index():
    """
    Test route
    """
    return JSONResponse({"status": "success"}, StatusCodes.CREATED.value)


@home_router.post("/hit-count")
async def hit_count():
    """
    Hit count route
    """
    ans, status_code = await update_visit_stats()
    return JSONResponse(ans, status_code)


@home_router.get("/get-testomonials")
async def get_testomonials():
    """
    Get testomonials route
    """
    ans, status_code = await fetch_testimonials()
    return JSONResponse({"testimonials_list": ans}, status_code)


# add async await everywhere inside the function
@home_router.post("/add-testimonial")
async def add_testimonial(
    name: str = Form(...),
    designation: str = Form(...),
    company: str = Form(...),
    feedback: str = Form(...),
    image: UploadFile = File(...)
):
    """
    Add testimonial route
    """
    testimonial_data = TestimonialFormat(
        name=name,
        designation=designation,
        company=company,
        feedback=feedback
    )
    # print("testimonial data", testimonial_data)
    # print("image", image)
    ans, status_code = await add_single_testimonial(testimonial_data, image)
    # TODO may use ans and status code
    return JSONResponse({"status": "success"}, StatusCodes.CREATED.value)

