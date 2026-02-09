from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import stripe

import logging

from app.core.config import config
# from app.api import subscription_tier_router
# from app.api import speaker_router
# from app.api import sub_speaker_router
# from app.api import subscription_router
# from app.api import generation_router
# from app.api import payment_router 
# from app.api import oauth_router
from app.ui import ui
# from app.api import audio_router
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
    # app.include_router(subscription_tier_router.router, prefix=f"/api/{api_version}")
    # app.include_router(speaker_router.router, prefix=f"/api/{api_version}")
    # app.include_router(sub_speaker_router.router, prefix=f"/api/{api_version}")
    # app.include_router(subscription_router.router, prefix=f"/api/{api_version}")
    # app.include_router(generation_router.router, prefix=f"/api/{api_version}")
    # app.include_router(payment_router.router, prefix=f"/api/{api_version}", include_in_schema=False)
    app.include_router(ui.router, include_in_schema=False)
    # app.include_router(oauth_router.router, prefix=f"/api/{api_version}")
    # app.include_router(audio_router.router, prefix=f"/api/{api_version}")

def setup_app(app: FastAPI):
    mount_static_directories(app)
    register_routers(app)
    register_exception_handlers(app)
    add_middleware(app)