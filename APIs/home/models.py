from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import MYSQL_URL


IST = pytz.timezone('Asia/Kolkata')
engine = create_async_engine(
    MYSQL_URL,
    pool_size = 5,
    max_overflow = 0,
    pool_timeout = 30,
    echo=True
)
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
Base = declarative_base()

class HitCount(Base):
    __tablename__ = "visit_stats"

    count = Column(Integer, primary_key=True, default=0)
    last_visit = Column(DateTime, default=datetime.now(IST))


class TempTable(Base):
    __tablename__ = "Temptable"

    col1 = Column(Integer, primary_key=True, default=1)
    col2 = Column(Integer, default=10)


class OneMore(Base):
    __tablename__ = "onemore"
    
    col = Column(Integer, primary_key=True, default=10)



class Testimonials(Base):
    __tablename__ = "testimonials"
    
    s_no = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    designation = Column(String(40), nullable=False)
    company = Column(String(30), nullable=False)
    feedback = Column(String(200), nullable=False)
    image_url = Column(String(100), nullable=True)




async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        # This will create the tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
