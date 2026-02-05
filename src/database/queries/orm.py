from database.engine_db import sync_engine, session_factory
from sqlalchemy import Integer, and_, or_, func, text, insert, select, update
from sqlalchemy.orm import aliased, joinedload, selectinload, join
from database.models import Base, SneakersOrm, ImagesOrm, SneakerSizesOrm
from schemas.filtersmodel import FilterModelDTO
from schemas.productcardmodel import ProductCardDTO, SneakersRelationDTO, SneakersViewRelationDTO

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
         # print(f"{sneakers}")
         
         result_dto = SneakersViewRelationDTO.model_validate(sneaker, from_attributes=True) 
      
         # print(f"{result_dto=}")
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






         