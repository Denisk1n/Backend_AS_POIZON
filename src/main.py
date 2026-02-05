from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from schemas.filtersmodel import FilterModelDTO
from database.queries.orm import SyncOrm
from schemas.productcardmodel import ProductCardDTO

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=['*'],
   allow_credentials=True,
   allow_methods=["*"], # Разрешить все методы: GET, POST, PUT, DELETE и т.д.
   allow_headers=["*"]
)

@app.post("/sneakers_with_filters", summary="Получаем фильтры с фронта и отдаем по этим фильтрам товары", response_model=list[ProductCardDTO])
def post_ProductCardsApplyingFilters(filters: FilterModelDTO):
   print(filters)
   result = SyncOrm.selectProductCardsWithFilters(filters)
   return result

@app.get("/sneakers", summary="Все карточки товара")
def get_AllSneakerCards():
   return SyncOrm.selectProductCards()


@app.get("/sneakers/{id}", summary="Полная информация о кроссовках")
def get_SneakerCard(id: int):
   return SyncOrm.selectProductInfo(id)


@app.get("/newsneakers", summary="Получение первых 4 карточек отсартированных по дате", response_model=list[ProductCardDTO])
def get_NewSneakerCards():
   return SyncOrm.selectNewSneakers()   




if __name__ == "__main__":
   uvicorn.run("main:app",reload=True)