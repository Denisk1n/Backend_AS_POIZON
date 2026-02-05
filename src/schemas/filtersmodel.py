from typing import Optional, Literal
from pydantic import BaseModel
from enum import Enum

class Sorted_by(Enum):
   default = "default"
   asc = "asc"
   desc = "desc"
   new = "new"
   

class FilterModelDTO(BaseModel):
   
   sizes: list[float]
   brands: list[str]
   available: list[Literal["В наличии", "Под заказ"]]
   price: Price
   sorted: Literal["default", "price-asc", "price-desc", "new"]


class Price(BaseModel):
   min: int
   max: int
   


