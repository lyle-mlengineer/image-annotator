from fastapi import FastAPI, status

from contextlib import asynccontextmanager
import logging

from app.core.config import config
from app.core.logging import setup_logging

from app.main_helpers import setup_app

setup_logging()

logging.info("Starting application...")
logging.info(f"Environment: {config.ENVIRONMENT}")

if config.ENVIRONMENT == "production":
    logging.warning("Running in production mode")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting application...")
    # init_app(app)
    yield

app = FastAPI(
    title=config.APP_NAME, 
    debug=config.DEBUG, 
    lifespan=lifespan, 
    summary=config.APP_SUMMARY,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    contact={"name": config.APP_CONTACT_NAME}
)

setup_app(app)

@app.get(
        "/health", 
        status_code=status.HTTP_200_OK, 
        response_model=dict, 
        tags=["Health"],
        summary="Health check",
        description="Health check",
        response_description="Health check"
        )
async def health_check():
    logging.info("Health check")
    return {"status": "ok"}

logging.info("Application started successfully.")