import traceback
from datetime import datetime

import pytz
from sqlalchemy import update

from config import MYSQL_URL
from Enum_data import StatusCodes
from utils.common_utils import handle_exception
from data_class.general import CustomException
from APIs.home.models import SessionLocal, HitCount
import platform


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
