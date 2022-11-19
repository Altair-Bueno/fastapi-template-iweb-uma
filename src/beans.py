'''
src/beans.py

@author Altair Bueno <altair.bueno@uma.es>
'''
from fastapi import Depends
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient

from .service import *

from .settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_mongo_client(config: Settings = Depends(get_settings)):
    # set a 5-second connection timeout
    return AsyncIOMotorClient(config.mongo.url, serverSelectionTimeoutMS=5000)


@lru_cache
def get_mongo_database(
    client=Depends(get_mongo_client), settings: Settings = Depends(get_settings)
):
    return client[settings.mongo.database]


@lru_cache
def get_usuario_collection(
    database=Depends(get_mongo_database), settings: Settings = Depends(get_settings)
):
    collection =  database[settings.mongo.usuario]
    # Create unique index for the collection's ID 
    #await collection.create_index(("telefono",pymongo.DESCENDING), unique=True)
    return collection

@lru_cache
def get_mensaje_collection(
    database=Depends(get_mongo_database), settings: Settings = Depends(get_settings)
):
    return database[settings.mongo.mensaje]

@lru_cache
def get_usuario_service(c = Depends(get_usuario_collection)):
    return UsuarioService(c)

@lru_cache
def get_mensaje_service(c = Depends(get_mensaje_collection)):
    return MensajeService(c)