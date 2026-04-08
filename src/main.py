from fastapi import FastAPI, Query
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from schemas.filtersmodel import FilterModelDTO
from database.queries.orm import AsyncOrm
from schemas.productcardmodel import ProductCardDTO

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=['*'],
   allow_credentials=True,
   allow_methods=["*"], # Разрешить все методы: GET, POST, PUT, DELETE и т.д.
   allow_headers=["*"]
)

@app.post("/sneakers_with_filters", 
          summary="Получаем фильтры с фронта и отдаем по этим фильтрам товары", 
          response_model=list[ProductCardDTO])
async def post_ProductCardsApplyingFilters(filters: FilterModelDTO):
   #print(filters)
   result = await AsyncOrm.selectProductCardsWithFilters(filters)
   return result

@app.get("/sneakers", summary="Все карточки товара", response_model=list[ProductCardDTO])
async def get_AllSneakerCards():
   result = await AsyncOrm.selectProductCards()
   return result


@app.get("/sneakers/{id}", summary="Полная информация о кроссовках")
async def get_SneakerCard(id: int):
   result = await AsyncOrm.selectProductInfo(id)
   return result 


@app.get("/newsneakers", summary="Получение первых 4 карточек отсартированных по дате", response_model=list[ProductCardDTO])
async def get_NewSneakerCards():
   result = await AsyncOrm.selectNewSneakers()  
   return  result 


@app.get("/recomended-sneakers", summary="Получение 8 рандмных карточек", response_model=list[ProductCardDTO])
async def get_RecomendedSneakers():
   result = await AsyncOrm.selectRecomendedSneakers()
   return result 


@app.get("/used-brands")
async def get_UsedBrands(): 
   result = await AsyncOrm.getUsedBrands()
   return result 


@app.get("/static-data")
async def get_staticData():
   result = await AsyncOrm.getStaticData()
   return result 




if __name__ == "__main__":
   uvicorn.run("main:app",reload=True)