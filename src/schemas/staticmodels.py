from typing import Optional, Literal
from pydantic import BaseModel

class AllSneakerSizesDTO(BaseModel):
   ru: float
   us: float
   sm: float 
   
class BrandsDTO(BaseModel):
   brand: str
   
   
class StaticDataDTO(AllSneakerSizesDTO, BrandsDTO):
   sneakerSizes = list["AllSneakerSizesDTO"]
   brands = list["BrandsDTO"]



   
