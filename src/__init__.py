'''
src/__init__.py

@author Altair Bueno <altair.bueno@uma.es>
'''
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from .routes import BaseRouter

__name__='Segundo parcial. Ingeniería web'
__version__='0.1.0'
__docs__='Altair Bueno Calvente. Software 4ºA'

app = FastAPI()
app.include_router(BaseRouter)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=__name__,
        version=__version__,
        description=__docs__,
        routes=app.routes,
    )

    # Include servers section
    openapi_schema["servers"] = [
        {"url": "/", "description": "Default"},
        {"url": "http://localhost:8000", "description": "Docker compose"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

