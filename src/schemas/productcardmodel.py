from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, field_validator
from decimal import Decimal


class SneakersPostDTO(BaseModel):
   title: str
   brand: str
   category: Literal["Кроссовки", "Одежда", "Аксессуары"]
   price: int
   main_image: str
   available: Literal["В наличии", "Под заказ"]
  
class SneakerProductCardDTO(SneakersPostDTO):
   id: int
   
class SneakersDTO(SneakersPostDTO):
   id: int    

class SneakersCreatedDTO(SneakersPostDTO):
   id: Optional[int] = None
   created_at: datetime = datetime.now()
   updated_at: datetime = datetime.now()
   
# для получения информации о продукте 
class SneakersRelationDTO(SneakersPostDTO):
   images: list["ImagesDTO"]
   sizes: list["SneakerSizesDTO"]

class SneakersViewRelationDTO(SneakersPostDTO):
   images: list["ImageViewDTO"]
   sizes: list["SneakerSizesViewDTO"]
   
   
   
# для добавления одной фотографии
class ImagesPostDTO(BaseModel):
   sneaker_id: int
   image: str
   position: int
   
# для просмотра на фронте
class ImageViewDTO(BaseModel):
   image: str
   position: int
   
class ImagesDTO(ImagesPostDTO):
   id: int
   
class ImagesCreatedDTO(ImagesPostDTO):
   created_at: datetime = datetime.now()
   updated_at: datetime = datetime.now()
   
class ImagesRelationDTO(ImagesDTO):
   sneaker: "SneakersDTO"



class SneakerSizesPostDTO(BaseModel):
   sneaker_id: int
   ru: float
   us: float
   sm: float
 
class SneakerSizesViewDTO(BaseModel):
   ru: float
   us: float
   sm: float 
   
class SneakerSizesDTO(SneakerSizesPostDTO):
   id: int 
   
class SneakerSizesCreatedDTO(SneakerSizesPostDTO):
   id: Optional[int] = None
   created_at: datetime = datetime.now()
   updated_at: datetime = datetime.now()
   
class SneakerSizesRelationDTO(SneakerSizesDTO):
   sneaker: "SneakersDTO"
