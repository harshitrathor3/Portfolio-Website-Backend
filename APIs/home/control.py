import random
import traceback
from datetime import datetime

import pytz
from fastapi import UploadFile
from sqlalchemy.future import select
from sqlalchemy import insert, update

from Enum_data import StatusCodes
from data_class.general import CustomException
from utils.image_utils import ImageUtils
from utils.common_utils import handle_exception
from APIs.home.payload_structure import TestimonialFormat
from APIs.home.models import SessionLocal, HitCount, Testimonials


# db = SessionLocal()


async def update_visit_stats():
    IST = pytz.timezone('Asia/Kolkata')
    try:
        async with SessionLocal() as db:
            async with db.begin():
                stmt = (
                    update(HitCount)
                    .values(count=HitCount.count+1, last_visit=datetime.now(IST))
                    .execution_options(synchronize_session="fetch")
                )
                result = await db.execute(stmt)
                if result.rowcount>0:
                    await db.commit()
                    return {"status": "success"}, StatusCodes.SUCCESS.value
                else:
                    return {"status": "failed"}, StatusCodes.EMPTY_RESPONSE.value
    except Exception as e:
        await db.rollback()
        # db.flush()
        # await db.close()
        custom_exception = CustomException(
            error_msg="error while updating visit stats table in hit_count route",
            data = {},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value



async def fetch_testimonials():
    result_list = []
    try:
        async with SessionLocal() as db:
            async with db.begin():
                stmt = (
                    select(Testimonials)
                )
                res = await db.execute(stmt)

                # TODO find way to directly get output as dictionary
                result = res.scalars().all()
                result_list = [
                    {
                        "s_no": row.s_no,
                        "name": row.name,
                        "designation": row.designation,
                        "company": row.company,
                        "feedback": row.feedback,
                        "image_url": row.image_url
                    }
                    for row in result
                ]
                return result_list, StatusCodes.SUCCESS.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while fetching testimonials",
            data = {},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
    finally:
        await db.close()


async def add_single_testimonial(testimonial_data: TestimonialFormat, image: UploadFile):
    try:
        async with SessionLocal() as db:
            async with db.begin():
                image_operations = ImageUtils(image)
                ans, status_code = image_operations.save_image_locally()

                if status_code != StatusCodes.CREATED.value:
                    print("image saving failed")
                    print("ans", ans)
                
                print("the image path is", image_operations.image_path)
                
                name_without_space = testimonial_data.name.replace(" ", "_")
                image_id_in_db = name_without_space + "_" + str(random.randint(1, 9999))
                ans, status_code = image_operations.upload_image(image_id_in_db)
                image_url = None
                if status_code == StatusCodes.CREATED.value:
                    image_url = ans["secure_url"]
                else:
                    print("image uploading failed")
                    print("ans", ans)

                print("image ans", ans)

                stmt = (
                    insert(Testimonials)
                    .values(
                        name=testimonial_data.name,
                        designation=testimonial_data.designation,
                        company=testimonial_data.company,
                        feedback=testimonial_data.feedback,
                        image_url=image_url
                    )
                )
                result = await db.execute(stmt)
                await db.commit()
                print("result", result)
                print("result.rowcount", result.rowcount)    
                print("testimonial data:", testimonial_data)
                print("image filename:", image.filename)
                print("image", image)
                return {"status": "success"}, StatusCodes.CREATED.value
    except Exception as e:
        custom_exception = CustomException(
            error_msg="error while adding single testimonial",
            data = {
                "testimonial data": testimonial_data,
                "image": image.filename
            },
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value
    finally:
        image_operations.delete_local_saved_image()
