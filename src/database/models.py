import datetime
from typing import Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship, Mapped, mapped_column # помогает для использования типов
from src.database.engine_db import Base
import enum


# Создаем кастомные типы данных
intpk = Annotated[int, mapped_column(primary_key=True)]
intfk = Annotated[int, mapped_column(ForeignKey("sneakers.id", ondelete="CASCADE"))]
created_at = Annotated[
   datetime.datetime, mapped_column(
      TIMESTAMP(timezone=False),
      server_default=text("CURRENT_TIMESTAMP(0)")
   )
]

# енумиратор 
class Availability(enum.Enum):
   open = "В наличии"
   close = "Под заказ"
   

#ORM - таблицы в Декларативном стиле 
class SneakersOrm(Base):
   __tablename__ = "sneakers"
   id: Mapped[intpk]
   title: Mapped[str]
   brand: Mapped[str]
   description: Mapped[str]
   price: Mapped[int]
   main_image: Mapped[str]
   available: Mapped[str]
   created_at: Mapped[created_at]
   
   images_sneaker: Mapped[list["Images_sneakerOrm"]] = relationship(
      back_populates="sneaker"
   )
   
   sizes_sneaker: Mapped[list["Sizes_sneakerOrm"]] = relationship(
      back_populates="sneaker"
   )
   


class Images_sneakerOrm(Base):
   __tablename__ = "images_sneaker"
   id: Mapped[intpk]
   sneaker_id: Mapped[intfk]
   sneaker_image: Mapped[str]
   
   sneaker: Mapped["SneakersOrm"] = relationship(
      back_populates="images_sneaker"
   )
   
   
   
class Sizes_sneakerOrm(Base):
   __tablename__ = "sizes_sneaker"
   id: Mapped[intpk]
   sneaker_id: Mapped[intfk]
   ru_size: Mapped[int]
   us_size: Mapped[int]
   sm_size: Mapped[int]
   
   sneaker: Mapped["SneakersOrm"] = relationship(
      back_populates="sizes_sneaker"
   )
   
