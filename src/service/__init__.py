'''
src/service/__init__.py

@author Altair Bueno <altair.bueno@uma.es>
'''

from typing import List
from ..model import *

class NotFound(BaseException):
    pass

class UsuarioService:
    def __init__(self, collection) -> None:
        self.collection = collection
    
    async def new(self, payload: NewUsuario) -> PyObjectId:
        document = payload.dict()
        document["contactos"] = []
        res = await self.collection.insert_one(document)

        return PyObjectId(res.inserted_id)

    
    async def update(self, telefono:str, payload: UpdateUsuario):
        res = await self.collection.update_one(
            {"telefono": telefono}, 
            {"$set": payload.dict(skip_defaults=True)}
        )

    async def delete(self, telefono: str):
        res = await self.collection.delete_one({"telefono": telefono})

    # Buscar un usuario de la red social a partir de su alias.
    async def get_all(self, alias: Optional[str] = None) -> List[Usuario]:
        f = {}

        if alias:
            f = f | {"alias": {"$regex": alias}}

        cursor = self.collection.find(f)
        return [Usuario(**x) async for x in cursor]

    async def get(self, telefono: str) -> Usuario:
        res = await self.collection.find_one({"telefono": telefono})
        return Usuario(**res)

    async def new_contacto(self, telefono: str, contacto: Contacto): 
        res = await self.collection.update_one({"telefono": telefono}, {"$push": {"contactos": contacto.dict()}})
    

    async def get_contactos(self, telefono: str, alias: Optional[str] = None) -> List[Contacto]: 
        pipeline = [
            {"$match": {"telefono": telefono}}
        ]

        if alias:
            pipeline.append({
                "$filter": {
                    "input": "$contactos",
                    "as": "contacto",
                    "cond": {
                        "$$contacto": {"$eq": alias}
                    },
                }
            })

        return [
            Contacto(**contacto) 
            async for x in self.collection.aggregate(pipeline) 
            for contacto in x["contactos"]
        ]


class MensajeService:
    def __init__(self, collection) -> None:
        self.collection = collection
    
    async def new(self, payload: NewMensaje):
        document = payload.dict()
        document["timestamp"] = datetime.now()
        res = await self.collection.insert_one(document)

    
    async def update(self, i: PyObjectId, payload: UpdateMensaje):
        res = await self.collection.update_one(
            {"_id": i}, 
            {"$set": payload.dict(skip_defaults=True)}
        )

    async def delete(self, i: PyObjectId):
        res = await self.collection.delete_one({"_id": i})

    # Buscar entre los mensajes enviados o recibidos por un usuario a partir de 
    # una cadena con parte de su texto, devolviendo una lista de mensajes.
    async def get_all(self, usuario: Optional[str] = None, texto: Optional[str] = None) -> List[Mensaje]:
        pipeline = [] 
        
        if usuario:
            pipeline.append({
                "$match": {
                    "$or": [
                        {"origen": usuario},
                        {"destino": usuario}
                    ]
                }
            })

        if texto:
            pipeline.append({"$match": {"texto": {"$regex": texto}}})
        
        cursor = self.collection.aggregate(pipeline)
        return [Mensaje(**x) async for x in cursor]

    async def get(self, i: PyObjectId) -> Mensaje:
        res = await self.collection.find_one({"_id": i})
        return Mensaje(**res)
