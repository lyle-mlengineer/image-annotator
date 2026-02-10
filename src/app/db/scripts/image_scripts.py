from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.exc import OperationalError, StatementError
from fastapi import HTTPException

import logging

from app.db.schema import Image
from app.models.image_model import ImageCreate, ImageUpdate
from app.core.config import config
from app.core.utils import generate_id

# Define which exceptions are transient and should trigger a retry
RETRYABLE_EXCEPTIONS = (OperationalError, StatementError)


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def create_image(image: ImageCreate, session: Session) -> Image:
    try:
        logging.info(f"Creating image with name: {image.image_name}")
        id: str = generate_id(prefix="IMAGE")
        new_image: Image = Image(
            id=id,
            image_name=image.image_name
        )
        session.add(new_image)
        session.commit()
        session.refresh(new_image)
        return new_image
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_image(image_id: str, session: Session) -> Image | None:
    try:
        image: Image = session.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()

@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_image_by_name(image_name: str, session: Session) -> Image | None:
    try:
        image: Image = session.query(Image).filter(Image.image_name == image_name).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()

@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_unlabelled_image(session: Session) -> Image | None:
    try:
        image: Image  = session.query(Image).filter(Image.status == "unlabelled").first()
        return image
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()

@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def delete_image(image_id: str, session: Session) -> None:
    try:
        logging.info(f"Deleting image with id: {image_id}")
        session.query(Image).filter(Image.id == image_id).delete()
        session.commit()
        logging.info(f"Deleted image with id: {image_id}")
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def update_image(image_id: str, image: ImageUpdate, session: Session) -> Image:
    try:
        logging.info(f"Updating image with id: {image_id}")
        image_to_update: Image = session.query(Image).filter(Image.id == image_id).first()
        if not image_to_update:
            raise HTTPException(status_code=404, detail="Image not found")
        image_to_update.image_name = image.image_name
        session.commit()
        session.refresh(image_to_update)
        return image_to_update
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_all_images(limit: int, offset: int, session: Session) -> list[Image]:
    try:
        if limit and offset:
            images: list[Image] = session.query(Image).limit(limit).offset(offset).all()
        else:
            images: list[Image] = session.query(Image).all()
        return images
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()