'''
src/routes/__init__.py

@author Altair Bueno <altair.bueno@uma.es>
'''
from typing import List
from fastapi import APIRouter, Depends

from ..model import *

from ..service import *
from ..beans import get_usuario_service, get_mensaje_service

BaseRouter = APIRouter()

mensajes = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@mensajes.get("", response_model=List[Mensaje])
async def get_all_mensajes(
    texto: Optional[str] = None,
    usuario: Optional[str] = None,
    s:MensajeService=Depends(get_mensaje_service)
):
    return await s.get_all(texto=texto,usuario=usuario)

@mensajes.get("/{id}", response_model=Mensaje)
async def get_mensaje(id:PyObjectId, s:MensajeService=Depends(get_mensaje_service)):
    return await s.get(id)

@mensajes.post("")
async def create_mensaje(payload:NewMensaje,s:MensajeService=Depends(get_mensaje_service)):
    return await s.new(payload)

@mensajes.put("/{id}")
async def update_mensaje(id:PyObjectId, payload:UpdateMensaje,s:MensajeService=Depends(get_mensaje_service)):
    return await s.update(id,payload)

@mensajes.delete("/{id}")
async def delete_mensaje(id: PyObjectId,s:MensajeService=Depends(get_mensaje_service)):
    return await s.delete(id)

BaseRouter.include_router(mensajes)



usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@usuarios.get("", response_model=List[Usuario])
async def get_all_usuarios(
    alias: Optional[str] = None,
    s:UsuarioService=Depends(get_usuario_service)
):
    return await s.get_all(alias=alias)

@usuarios.get("/{telefono}", response_model=Usuario)
async def get_usuario(telefono:str,s:UsuarioService=Depends(get_usuario_service)):
    return await s.get(telefono)

@usuarios.post("", response_model=NewUsuarioResponse)
async def create_usuario(payload:NewUsuario,s:UsuarioService=Depends(get_usuario_service)):
    res = await s.new(payload)
    return NewUsuarioResponse(id=res)

@usuarios.put("/{telefono}")
async def update_usuario(telefono: str, payload:UpdateUsuario,s:UsuarioService=Depends(get_usuario_service)):
    return await s.update(telefono,payload)

@usuarios.delete("/{telefono}")
async def delete_usuario(telefono: str, s: UsuarioService=Depends(get_usuario_service)):
    return await s.delete(telefono)

@usuarios.get("/{telefono}/contactos", response_model=List[Contacto])
async def get_contactos(telefono: str, s: UsuarioService=Depends(get_usuario_service)):
    return await s.get_contactos(telefono)

@usuarios.post("/{telefono}/contactos")
async def create_contacto(telefono: str, payload: Contacto, s: UsuarioService=Depends(get_usuario_service)):
    return await s.new_contacto(telefono, payload)

BaseRouter.include_router(usuarios)
