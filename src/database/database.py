from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  
from sqlalchemy import create_engine, text 
from config import settings


# создаем движок для работы с БД
sync_engine = create_engine(
   url=settings.DATABASE_URL_psycopg,
   echo=True,
   pool_size=5,
   max_overflow=10
)


# базовая сессря для подключения 
session_factory = sessionmaker(sync_engine)