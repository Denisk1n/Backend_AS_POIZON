import datetime
from typing import Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship, Mapped, mapped_column # помогает для использования типов
from database.engine_db import Base
import enum


# Создаем кастомные типы данных
intpk = Annotated[int, mapped_column(primary_key=True)]
intfk = Annotated[int, mapped_column(ForeignKey("sneakers.id", ondelete="CASCADE"))]
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.now())]
updated_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.now())]


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
   category: Mapped[str]
   description: Mapped[str]
   price: Mapped[int]
   main_image: Mapped[str]
   available: Mapped[str]
   created_at: Mapped[created_at]
   updated_at: Mapped[created_at]
   
   images: Mapped[list["ImagesOrm"]] = relationship(
      back_populates="sneaker"
   )
   
   sizes: Mapped[list["SneakerSizesOrm"]] = relationship(
      back_populates="sneaker"
   )
   


class ImagesOrm(Base):
   __tablename__ = "images"
   id: Mapped[intpk]
   sneaker_id: Mapped[intfk]
   position: Mapped[int]
   image: Mapped[str]
   created_at: Mapped[created_at]
   updated_at: Mapped[created_at]
   
   sneaker: Mapped["SneakersOrm"] = relationship(
      back_populates="images"
   )
   
   
   
class SneakerSizesOrm(Base):
   __tablename__ = "sneakersizes"
   id: Mapped[intpk]
   sneaker_id: Mapped[intfk]
   ru: Mapped[float]
   us: Mapped[float]
   sm: Mapped[float]
   
   created_at: Mapped[created_at]
   updated_at: Mapped[created_at]
   
   sneaker: Mapped["SneakersOrm"] = relationship(
      back_populates="sizes"
   )
   

class AllSneakerSizes(Base):
   __tablename__ = "allsizes"
   id: Mapped[intpk]
   ru: Mapped[float]
   us: Mapped[float]
   sm: Mapped[float]
   
   created_at: Mapped[created_at]
   updated_at: Mapped[created_at]
   

class AllBrands(Base):
   __tablename__ = "allbrands"
   id: Mapped[intpk]
   brand: Mapped[str]

   created_at: Mapped[created_at]
   updated_at: Mapped[created_at]
   

   