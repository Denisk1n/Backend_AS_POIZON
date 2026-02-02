from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from database.queries.orm import SyncOrm

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=['*']
)


@app.get("/sneakers", summary="Информация на карточке товара")
def get_all_sneakers_card():
   return SyncOrm.selectProductCard()




@app.get("/sneakers/{id}", summary="Полная информация о кроссовках")
def get_SneakerCard(id: int):
   return SyncOrm.selectProductInfo(id)



if __name__ == "__main__":
   uvicorn.run("main:app",reload=True)