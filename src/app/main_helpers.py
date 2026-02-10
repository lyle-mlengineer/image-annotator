from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import logging

from app.core.config import config
from app.ui import ui
from app.api import image_router
from app.api import user_router
from app.exception_handlers import register_exception_handlers
 
def mount_static_directories(app: FastAPI):
    app.mount(
        "/static", 
        StaticFiles(directory=config.STATIC_DIR), 
        name="static"
        )
    app.mount(
        "/data", 
        StaticFiles(directory=config.DATA_DIR), 
        name="data"
    )

def add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_routers(app: FastAPI):
    api_version: str = config.API_VERSION
    app.include_router(ui.router, include_in_schema=False)
    app.include_router(image_router.router, prefix=f"/api/{api_version}/images")
    app.include_router(user_router.router, prefix=f"/api/{api_version}/users")

def setup_app(app: FastAPI):
    mount_static_directories(app)
    register_routers(app)
    register_exception_handlers(app)
    add_middleware(app)