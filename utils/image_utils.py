import os
import random
import traceback

import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile

from Enum_data import StatusCodes
from utils.common_utils import handle_exception
from data_class.general import CustomException
from config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME




class ImageUtils:
    def __init__(self, image: UploadFile) -> None:
        # Configuration       
        cloudinary.config( 
            cloud_name = CLOUDINARY_CLOUD_NAME, 
            api_key = CLOUDINARY_API_KEY, 
            api_secret = CLOUDINARY_API_SECRET,
            secure=True
        )
        self.image = image
        self.image_path = ""


    def save_image_locally(self):
        """
        Save image locally

        Args:
            image (UploadFile): image file

        Returns:
            image_path (str): path of image
            status_code (int): status of the operation
        """
        try:
            image_filename = self.image.filename
            image_filename_without_ext, ext = os.path.splitext(image_filename)
            image_filename_final = f"{image_filename_without_ext}_{random.randint(1, 9999)}{ext}"
            with open(image_filename_final, "wb") as buffer:
                buffer.write(self.image.file.read())
            self.image_path = os.path.abspath(image_filename_final)

            return {"status": "success"}, StatusCodes.CREATED.value
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def upload_image(self, public_id: str):
        """
        Upload an image to cloudinary

        Args:
            public_id (str): image unique id

        Returns:
            _type_: 
        """
        try:
            upload_result = cloudinary.uploader.upload(self.image_path, secure=True, public_id=public_id)
            return upload_result, StatusCodes.CREATED.value
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {
                    "public_id": public_id
                },
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def optimize_image(self, public_id: str):
        """
        Optimize delivery by resizing and applying auto-format and auto-quality

        Args:
            public_id (str): image unique id

        Returns:
            _type_: 
        """
        try:
            optimize_url, _ = cloudinary_url(public_id, fetch_format="auto", quality="auto")
            return optimize_url
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def transform_image(self, public_id: str, width: int, height: int):
        """
        Transform the image: auto-crop to square aspect_ratio

        Args:
            public_id (str): image unique id
            width (int): image width
            height (int): image height

        Returns:
            _type_: 
        """
        try:
            auto_crop_url, _ = cloudinary_url(public_id, width=width, height=height, crop="auto", gravity="auto")
            return auto_crop_url
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def get_image_info(self, public_id: str):
        """
        Get image info from cloudinary

        Args:
            public_id (str): image unique id

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.resource(public_id)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_image(self, public_id: str):
        """
        Delete image from cloudinary

        Args:
            public_id (str): image unique id

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_resources(public_id)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_all_images(self):
        """
        Delete all images from cloudinary

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_all_resources()
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_all_images_by_prefix(self, prefix: str):
        """
        Delete all images from cloudinary by prefix

        Args:
            prefix (str): image prefix

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_resources_by_prefix(prefix)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_all_images_by_tag(self, tag: str):
        """
        Delete all images from cloudinary by tag

        Args:
            tag (str): image tag

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_resources_by_tag(tag)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_all_images_by_ids(self, public_ids: list):
        """
        Delete all images from cloudinary by ids

        Args:
            public_ids (list): image ids

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_resources(public_ids)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value


    def delete_all_images_by_tag(self, tag: str):
        """
        Delete all images from cloudinary by tag

        Args:
            tag (str): image tag

        Returns:
            _type_: 
        """
        try:
            image_info=cloudinary.api.delete_resources_by_tag(tag)
            return image_info
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
    

    def delete_local_saved_image(self):
        """
        Delete local saved image

        Args:
            image_path (str): image path

        Returns:
            _type_: 
        """
        try:
            if os.path.exists(self.image_path):
                os.remove(self.image_path)
                print("locally saved image deleted")
        except Exception as e:
            custom_exception = CustomException(
                error_msg="error while fetching testimonials",
                data = {},
                exception=str(e),
                trace=traceback.format_exc()
            )
            exception_ans = handle_exception(custom_exception)
            return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value



