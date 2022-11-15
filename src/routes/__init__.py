'''
src/routes/__init__.py

@author Altair Bueno <altair.bueno@uma.es>
'''
from fastapi import APIRouter, Depends
from ..beans import get_collection

BaseRouter = APIRouter()

@BaseRouter.get("/example")
async def example(collection=Depends(get_collection)):
    return [x async for x in collection.find({})]