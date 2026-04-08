from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase  
from sqlalchemy import create_engine, text 
from database.config import settings


# создаем движок для работы с БД
sync_engine = create_engine(
   url=settings.DATABASE_URL_psycopg,
   echo=False
   # pool_size=5,
   # max_overflow=10
)

# асинхронныц движок
async_engine = create_async_engine(
   url=settings.DATABASE_URL_asyncpg,
   echo=False
)



# базовая сессря для подключения 
session_factory = sessionmaker(sync_engine)

# асинхронная сессия для подключения 
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
   pass