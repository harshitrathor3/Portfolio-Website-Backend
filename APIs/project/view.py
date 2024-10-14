from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Form, File, UploadFile

from Enum_data import StatusCodes
from APIs.project.control import predict_digit_in_image

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/")
async def fun():
    """
    Test route
    """
    return JSONResponse({"status": "yep succes"}, StatusCodes.CREATED.value)



# AI ML Project Routes

@project_router.post("/digit-classification")
async def digit_classification(
    key1: str = Form(...),
    key2: str = Form(...),
    image_to_test: UploadFile = File(...)
):
    """
    Digit Classification Project
    """

    output, status_code = await predict_digit_in_image(image_to_test)

    return JSONResponse({"output": output}, status_code)

@project_router.post("/titanic-survival-prediction")
def titanic_survival_prediction(
    passenger_data: str = Form(...)
):
    """
    Titanic Survival Prediction Project
    """

    print("passenger data", passenger_data)

    return JSONResponse({"survival_probability": 0.85}, StatusCodes.SUCCESS.value)


@project_router.post("/california-housing-value-prediction")
def california_housing_value_prediction(
    housing_data: str = Form(...)
):
    """
    California Housing Value Prediction Project
    """

    print("housing data", housing_data)

    return JSONResponse({"predicted_value": 350000}, StatusCodes.SUCCESS.value)


@project_router.post("/horse-human-classifier")
def horse_human_classifier(
    image_to_test: UploadFile = File(...)
):
    """
    Horse Human Classifier Project
    """

    print("image", image_to_test)

    return JSONResponse({"classification": "horse"}, StatusCodes.SUCCESS.value)


@project_router.post("/happy-sad-emoji-classifier")
def happy_sad_emoji_classifier(
    image_to_test: UploadFile = File(...)
):
    """
    Happy Sad Emoji Classifier Project
    """

    print("image", image_to_test)

    return JSONResponse({"classification": "happy"}, StatusCodes.SUCCESS.value)

