from datetime import datetime
from typing import AsyncGenerator

from fastapi.params import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
        id =  Column(Integer, primary_key=True)
        username = Column(String, nullable=False) 
        email: str = Column(String(length=320), unique=True, index=True, nullable=False       )
        hashed_password: str = Column(String(length=1024), nullable=False )
        is_active: bool = Column(Boolean, default=True, nullable=False)
        is_superuser: bool = Column(Boolean, default=False, nullable=False)
        is_verified: bool = Column(Boolean, default=False, nullable=False)

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)