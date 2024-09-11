import traceback
from datetime import datetime

import pytz
from sqlalchemy import update
from sqlalchemy.future import select

from config import MYSQL_URL
from Enum_data import StatusCodes
from utils.common_utils import handle_exception
from data_class.general import CustomException
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
                        "image_id": row.image_id
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
