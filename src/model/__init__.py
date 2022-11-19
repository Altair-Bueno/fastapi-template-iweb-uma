'''
src/model/__init__.py

@author Altair Bueno <altair.bueno@uma.es>
'''

from datetime import datetime
from typing import List, Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, constr

class PyObjectId(ObjectId):
    """Wrapper around `pymongo`'s `ObjectId` class for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Contacto(BaseModel):
    alias: str
    telefono: str

class Usuario(BaseModel):
    telefono: str
    alias: str
    contactos: List[Contacto] = []

class NewUsuario(BaseModel):
    telefono: str
    alias: str

class UpdateUsuario(BaseModel):
    alias: Optional[str]


class Mensaje(BaseModel):
    id: PyObjectId = Field(alias="_id")
    timestamp: datetime
    origen: str
    destino: str
    texto: constr(max_length=400)

    class Config:
        json_encoders = {ObjectId: str}

class NewMensaje(BaseModel):
    origen: str
    destino: str
    texto: constr(max_length=400)

    class Config:
        json_encoders = {ObjectId: str}

class UpdateMensaje(BaseModel):
    texto: constr(max_length=400)

    class Config:
        json_encoders = {ObjectId: str}


class NewUsuarioResponse(BaseModel):
    id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}