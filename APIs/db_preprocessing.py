import traceback

from sqlalchemy.future import select

from utils.common_utils import handle_exception
from data_class.general import CustomException
from Enum_data import StatusCodes
from APIs.home.models import create_tables, engine, SessionLocal, TempTable, OneMore




async def insert_default_row_in_table():
    try:
        async with SessionLocal() as db:
            result = await db.execute(select(TempTable))
            res1 = await db.execute(select(OneMore))
            row = result.first()
            row1 = res1.first()

            if row is None:
                default_row = TempTable(col1=1, col2=10)
                db.add(default_row)
                await db.commit()
                print("Inserted default row (1, 10) into TempTable.")

            if not row1:
                default_row = OneMore(col=100)
                db.add(default_row)
                await db.commit()
                print("row inserted in one more table")
    except Exception as e:
        await db.rollback()
        custom_exception = CustomException(
            error_msg="error while updating visit stats table in hit_count route",
            data = {},
            exception=str(e),
            trace=traceback.format_exc()
        )
        exception_ans = handle_exception(custom_exception)
        return {"error": exception_ans}, StatusCodes.INTERNAL_SERVER_ERROR.value




async def db_preparation():
    await create_tables(engine)
    await insert_default_row_in_table()

