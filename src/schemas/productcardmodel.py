from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict



class SneakersPostDTO(BaseModel):
   title: str
   brand: str
   price: int
   main_image: str
   available: str
  
class SneakerProductCardDTO(SneakersPostDTO):
   id: int
   
class SneakersDTO(SneakersPostDTO):
   id: int 
   created_at: datetime
   
class SneakersRelationDTO(SneakersDTO):
   images_sneaker: list["Images_sneakerDTO"]
   sizes_sneaker: list["Sizes_sneakerDTO"]
   


class Images_sneakerPostDTO(BaseModel):
   sneaker_id: int
   sneaker_image: str
   
class Images_sneakerDTO(Images_sneakerPostDTO):
   id: int
   
class Images_sneakerRelationDTO(Images_sneakerDTO):
   sneaker: "SneakersDTO"



class Sizes_sneakerPostDTO(BaseModel):
   sneaker_id: int
   ru_size: int
   us_size: int
   sm_size: int
   
class Sizes_sneakerDTO(Sizes_sneakerPostDTO):
   id: int 
   
class Sizes_sneakerRelationDTO(Sizes_sneakerDTO):
   sneaker: "SneakersDTO"
