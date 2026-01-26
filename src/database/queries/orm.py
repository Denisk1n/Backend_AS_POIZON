from src.database.engine_db import sync_engine, session_factory
from sqlalchemy import Integer, and_, cast, func, text, insert, select, update
from sqlalchemy.orm import aliased, joinedload, selectinload
from src.database.models import Base, SneakersOrm, Images_sneakerOrm, Sizes_sneakerOrm


sneakers_data = [
    {
        "title": "Nike Blazer Low Jumbo",
        "brand": "Nike",
        "description": "Инновационные кроссовки с амортизирующей подошвой",
        "price": 12999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/best_blazer_25x16.jpg",
        "available": "В наличии"
    },
    {
        "title": "Dunk Low Etro Prm Graffiti",
        "brand": "Nike",
        "description": "Беговые кроссовки с технологией Boost",
        "price": 14999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/Dunk_low_2.png",
        "available": "В наличии"
    },
    {
        "title": "Dunk Low Grey",
        "brand": "Nike",
        "description": "Классические кроссовки для повседневной носки",
        "price": 8999,
        "main_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/Dunk_low_3.png",
        "available": "Под заказ"
    }
]

images_sneaker_data = [
    { "sneaker_id": 1, "sneaker_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_1.jpg"},
    { "sneaker_id": 1, "sneaker_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_2.jpg"},
    { "sneaker_id": 1, "sneaker_image": "https://bb5cb8d5-a455-46c6-a77c-1567031ec1a7.selstorage.ru/Backend_images/blazer_3.jpg"},
]

sizes_sneaker_data = [
    # Nike Air Max 270 - 5 размеров
    { "sneaker_id": 1, "ru_size": 40, "us_size": 7, "sm_size": 25},
    { "sneaker_id": 1, "ru_size": 41, "us_size": 8, "sm_size": 26},
    { "sneaker_id": 1, "ru_size": 42, "us_size": 9, "sm_size": 27},
    { "sneaker_id": 1, "ru_size": 43, "us_size": 10, "sm_size": 28},
    { "sneaker_id": 1, "ru_size": 44, "us_size": 11, "sm_size": 29},
    
    # Adidas Ultraboost 22 - 5 размеров
    { "sneaker_id": 2, "ru_size": 39, "us_size": 6, "sm_size": 24},
    { "sneaker_id": 2, "ru_size": 40, "us_size": 7, "sm_size": 25},
    { "sneaker_id": 2, "ru_size": 41, "us_size": 8, "sm_size": 26},
    { "sneaker_id": 2, "ru_size": 42, "us_size": 9, "sm_size": 27},
    { "sneaker_id": 2, "ru_size": 43, "us_size": 10, "sm_size": 28},
    
    # New Balance 574 - 5 размеров
    { "sneaker_id": 3, "ru_size": 38, "us_size": 5, "sm_size": 23},
    { "sneaker_id": 3, "ru_size": 39, "us_size": 6, "sm_size": 24},
    { "sneaker_id": 3, "ru_size": 40, "us_size": 7, "sm_size": 25},
    { "sneaker_id": 3, "ru_size": 41, "us_size": 8, "sm_size": 26},
    { "sneaker_id": 3, "ru_size": 42, "us_size": 9, "sm_size": 27}
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
         image_instance = Images_sneakerOrm(**image)
         images_instances.append(image_instance)
      
      session.add_all(images_instances)
      
      # Добавляем размеры
      sizes_instances = []
      for size in sizes_sneaker_data:
         size_instance = Sizes_sneakerOrm(**size)
         sizes_instances.append(size_instance)
      
      session.add_all(sizes_instances)
      session.commit()

         