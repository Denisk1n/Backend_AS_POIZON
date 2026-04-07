from database.engine_db import sync_engine, session_factory
from fastapi import Query
from typing import Optional
from sqlalchemy import Integer, and_, or_, func, text, insert, select, update
from sqlalchemy.orm import aliased, joinedload, selectinload, join
from database.models import Base, SneakersOrm, ImagesOrm, SneakerSizesOrm, AllSneakerSizes, AllBrands
from schemas.filtersmodel import FilterModelDTO
from schemas.productcardmodel import ProductCardDTO, SneakersRelationDTO, SneakersViewRelationDTO, ImageViewDTO
from schemas.staticmodels import StaticDataDTO, AllSneakerSizesDTO, BrandsDTO

sneakers_data = [
    {
        "title": "Nike Blazer Low Jumbo",
        "brand": "Nike",
        "category": "Кроссовки",
        "description": "Инновационные кроссовки с амортизирующей подошвой",
        "price": 12999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/best_blazer_25x16.jpg",
        "available": "В наличии"
    },
    {
        "title": "Dunk Low Etro Prm Graffiti",
        "brand": "Nike",
        "category": "Кроссовки",
        "description": "Беговые кроссовки с технологией Boost",
        "price": 14999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/Dunk_low_2.png",
        "available": "В наличии"
    },
    {
        "title": "Dunk Low Grey",
        "brand": "Nike",
        "category": "Кроссовки",
        "description": "Классические кроссовки для повседневной носки",
        "price": 8999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/Dunk_low_3.png",
        "available": "Под заказ"
    }
]

images_sneaker_data = [
    { "sneaker_id": 1, "position": 1, "image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_1.jpg"},
    { "sneaker_id": 1, "position": 2, "image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_2.jpg"},
    { "sneaker_id": 1, "position": 3, "image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_3.jpg"},
]

sizes_sneaker_data = [
    # Nike Air Max 270 - 5 размеров
    { "sneaker_id": 1, "ru": 40.5, "us": 7, "sm": 25},
    { "sneaker_id": 1, "ru": 41, "us": 8, "sm": 26},
    { "sneaker_id": 1, "ru": 42, "us": 9, "sm": 27},
    { "sneaker_id": 1, "ru": 43, "us": 10, "sm": 28},
    { "sneaker_id": 1, "ru": 44, "us": 11, "sm": 29},
    
    # Adidas Ultraboost 22 - 5 размеров
    { "sneaker_id": 2, "ru": 39, "us": 6, "sm": 24},
    { "sneaker_id": 2, "ru": 40, "us": 7, "sm": 25},
    { "sneaker_id": 2, "ru": 41, "us": 8, "sm": 26},
    { "sneaker_id": 2, "ru": 42, "us": 9, "sm": 27},
    { "sneaker_id": 2, "ru": 43, "us": 10, "sm": 28},
    
    # New Balance 574 - 5 размеров
    { "sneaker_id": 3, "ru": 38, "us": 5, "sm": 23},
    { "sneaker_id": 3, "ru": 39, "us": 6, "sm": 24},
    { "sneaker_id": 3, "ru": 40, "us": 7, "sm": 25},
    { "sneaker_id": 3, "ru": 41, "us": 8, "sm": 26},
    { "sneaker_id": 3, "ru": 42, "us": 9, "sm": 27}
]

all_sizes = [
    {"ru": 37.5, "us": 5, "sm": 22.9},
    {"ru": 38, "us": 5.5, "sm": 23.3},
    {"ru": 38.5, "us": 6, "sm": 23.8},
    {"ru": 39, "us": 6.5, "sm": 24.2},
    {"ru": 39.5, "us": 7, "sm": 24.6},
    {"ru": 40, "us": 7.5, "sm": 25.0},
    {"ru": 41, "us": 8, "sm": 25.5},
    {"ru": 41.5, "us": 8.5, "sm": 26.0},
    {"ru": 42, "us": 9, "sm": 26.3},
    {"ru": 43, "us": 9.5, "sm": 26.7},
    {"ru": 43.5, "us": 10, "sm": 27.1},
    {"ru": 44, "us": 10.5, "sm": 27.6},
    {"ru": 45, "us": 11, "sm": 28.0},
    {"ru": 45.5, "us": 11.5, "sm": 28.4},
    {"ru": 46, "us": 12, "sm": 28.8},
    {"ru": 47, "us": 12.5, "sm": 29.3},
    {"ru": 47.5, "us": 13, "sm": 29.7},
    {"ru": 48, "us": 13.5, "sm": 30.1},
    {"ru": 49, "us": 14, "sm": 30.5},
]

all_brands = [
    # Спортивная обувь и одежда (основные)
    {"brand": "Nike"},
    {"brand": "Adidas"},
    {"brand": "Puma"},
    {"brand": "Reebok"},
    {"brand": "New Balance"},
    {"brand": "Asics"},
    {"brand": "Under Armour"},
    {"brand": "Mizuno"},
    {"brand": "Saucony"},
    {"brand": "Brooks"},
    
    # Баскетбольные бренды
    {"brand": "Jordan"},
    {"brand": "And1"},
    {"brand": "Li-Ning"},
    {"brand": "Anta"},
    
    # Стритвир и lifestyle
    {"brand": "Vans"},
    {"brand": "Converse"},
    {"brand": "Supreme"},
    {"brand": "Stussy"},
    {"brand": "Off-White"},
    {"brand": "Bape"},
    {"brand": "Palace"},
    {"brand": "Kith"},
    
    # Люкс и дизайнерские
    {"brand": "Balenciaga"},
    {"brand": "Gucci"},
    {"brand": "Louis Vuitton"},
    {"brand": "Dior"},
    {"brand": "Versace"},
    {"brand": "Givenchy"},
    {"brand": "Alexander McQueen"},
    {"brand": "Saint Laurent"},
    {"brand": "Rick Owens"},
    {"brand": "Maison Margiela"},
    
    # Функциональная одежда
    {"brand": "The North Face"},
    {"brand": "Patagonia"},
    {"brand": "Columbia"},
    {"brand": "Arc'teryx"},
    {"brand": "Salomon"},
    {"brand": "Carhartt"},
    {"brand": "Dickies"},
    
    # Аксессуары и сумки
    {"brand": "Herschel"},
    {"brand": "Fjallraven"},
    {"brand": "Eastpak"},
    {"brand": "JanSport"},
    {"brand": "Osprey"},
    
    # Часы
    {"brand": "Casio"},
    {"brand": "G-Shock"},
    {"brand": "Timex"},
    {"brand": "Seiko"},
    {"brand": "Apple Watch"},
    {"brand": "Samsung"},
    
    # Носки и аксессуары
    {"brand": "Stance"},
    {"brand": "Happy Socks"},
    {"brand": "Injinji"},
    
    # Российские бренды
    {"brand": "Outventure"},
    {"brand": "Forward"},
    {"brand": "Nordman"},
    {"brand": "Sivera"},
    {"brand": "Kari"},
    {"brand": "Zenden"},
    {"brand": "Ralf Ringer"},
    
    # Другие популярные
    {"brand": "Fila"},
    {"brand": "Lacoste"},
    {"brand": "Tommy Hilfiger"},
    {"brand": "Calvin Klein"},
    {"brand": "Champion"},
    {"brand": "H&M"},
    {"brand": "Zara"},
    {"brand": "Uniqlo"},
    {"brand": "Decathlon"},
    {"brand": "Skechers"},
    {"brand": "Crocs"},
    {"brand": "Timberland"},
    {"brand": "Dr. Martens"},
    {"brand": "Clarks"},
    {"brand": "Ecco"},
    {"brand": "Geox"},
]
class SyncOrm:
   
   @staticmethod
   def create_tables():
      sync_engine.echo = True
      Base.metadata.drop_all(sync_engine)
      Base.metadata.create_all(sync_engine)
      sync_engine.echo = False


   @staticmethod
   def insert_test_data():
      with session_factory() as session:
         sneakers = []
         for sn in sneakers_data:
            sneaker = SneakersOrm(**sn)
            sneakers.append(sneaker)
      
      session.add_all(sneakers)
      session.commit()
    
      # Добавляем фотографии
      images_instances = []
      for image in images_sneaker_data:
         image_instance = ImagesOrm(**image)
         images_instances.append(image_instance)
      
      session.add_all(images_instances)
      
      # Добавляем размеры
      sizes_instances = []
      for size in sizes_sneaker_data:
         size_instance = SneakerSizesOrm(**size)
         sizes_instances.append(size_instance)
      
      session.add_all(sizes_instances)
      session.commit()
      
   
   @staticmethod
   def insert_static_data():
      with session_factory() as session:
         
         sizes = [AllSneakerSizes(**size) for size in all_sizes]
         brands = [AllBrands(**brand) for brand in all_brands]
         
         session.add_all(sizes)
         session.add_all(brands)
         
         session.commit()
         
         print(f"Добавленно: {len(sizes)} размеров и {len(brands)} брендов" )
         
   
   
   @staticmethod
   def selectProductCards():
      with session_factory() as session:
         
         query = select(SneakersOrm)

         result = session.execute(query)
         sneakers = result.scalars().all()
         # print(f"{sneakers}")
         
         result_dto = [ProductCardDTO.model_validate(row, from_attributes=True) for row in sneakers]
      
         # print(f"{result_dto=}")
         return result_dto
   
   
   # полные данные об одной карточке - страница товара 
   @staticmethod
   def selectProductInfo(id):
      with session_factory() as session:
         
         query = (
            select(SneakersOrm)
            .options(selectinload(SneakersOrm.images))
            .options(selectinload(SneakersOrm.sizes))
            .where(SneakersOrm.id == id)
         )

         result = session.execute(query)
         sneaker = result.scalars().one()
         # print(f"{sneaker}")
         
         result_dto = SneakersViewRelationDTO.model_validate(sneaker, from_attributes=True) 
         
         # result_dto.images.append(ImageViewDTO(image=f"{result_dto.main_image}", position=0))
         # print(f"{result_dto.images}")
         return result_dto


   # запрос на 4 самые новые товара кроссовок для начального 
   @staticmethod
   def selectNewSneakers():
      with session_factory() as session:
         
         query = (
            select(SneakersOrm)
            .order_by(SneakersOrm.updated_at.desc())
            .limit(4)
         )
         
         result = session.execute(query)
         sneakers = result.scalars().all()
         resultDTO = [ProductCardDTO.model_validate(row, from_attributes=True) for row in sneakers]
         return resultDTO
      
      
   # в зависимости от фильтров отдаем карточки товаров 
   @staticmethod
   def selectProductCardsWithFilters(filters: FilterModelDTO):
      with session_factory() as session:
         
         brands = filters.brands
         available = filters.available
         price = filters.price
         sizes = filters.sizes
         sorted = filters.sorted
         
         query = (
            select(SneakersOrm).distinct()
            .join(SneakerSizesOrm, SneakerSizesOrm.sneaker_id == SneakersOrm.id, isouter=True)
            .join(ImagesOrm, ImagesOrm.sneaker_id == SneakersOrm.id, isouter=True)
            )
         
         if price:
            query = query.filter(SneakersOrm.price >= price.min)
            query = query.filter(SneakersOrm.price <= price.max)

         if brands:
            query = query.filter(SneakersOrm.brand.in_(brands))

         if available:
            query = query.filter(SneakersOrm.available.in_(available))
            
         if sizes:
            query = query.filter(SneakerSizesOrm.ru.in_(sizes))
         
         match sorted:
               case "default":
                  query 
               case "new":
                  query = query.order_by(SneakersOrm.updated_at.desc())
               case "price-asc":
                  query = query.order_by(SneakersOrm.price.asc())
               case "price-desc":
                  query = query.order_by(SneakersOrm.price.desc())
               case _:
                  query

         # print(query)
         result = session.execute(query)
         sneakers = result.scalars().all()
         
         result_dto = [ProductCardDTO.model_validate(row, from_attributes=True) for row in sneakers]
         return result_dto


   # рекомендуемые кроссовки 
   @staticmethod
   def selectRecomendedSneakers():
      with session_factory() as session:
         
         query = (
            select(SneakersOrm)
            .order_by(func.random())
            .limit(2)
         )
         
         result = session.execute(query)
         sneakers = result.scalars().all()
         
         result_dto = [ProductCardDTO.model_validate(row, from_attributes=True) for row in sneakers]
         return result_dto


   # использованные бренды
   @staticmethod
   def getUsedBrands():
      with session_factory() as session:
         
         query = (
            select(SneakersOrm.brand)
            .distinct(SneakersOrm.brand)
         )
         
         result = session.execute(query)
         brands = result.scalars().all()
         
         res = [ {"label": brand, "value": brand} for brand in brands ]
         
         return res
   
   
   # статические данные
   @staticmethod 
   def getStaticData():
      with session_factory() as session:
         
         
         sizes_query = session.execute(select(AllSneakerSizes))
         brands_query = session.execute(select(AllBrands))
         
         sizes = sizes_query.scalars().all()
         brands = brands_query.scalars().all()
         
         sizes_dto = [AllSneakerSizesDTO.model_validate(row, from_attributes=True) for row in sizes]
         brands_dto = [BrandsDTO.model_validate(row, from_attributes=True) for row in brands]
         

         return StaticDataDTO(
            sneakerSizes= sizes_dto,
            brands= brands_dto
         )