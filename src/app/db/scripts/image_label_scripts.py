from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.exc import OperationalError, StatementError
from fastapi import HTTPException

import logging

from app.db.schema import ImageLabel, Image
from app.models.image_label_model import ImageLabelCreate, ImageLabelUpdate
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
def create_image_label(image_label: ImageLabelCreate, session: Session) -> ImageLabel:
    try:
        logging.info(f"Creating image label with name: {image_label.image_name}")
        image: Image = session.query(Image).filter(Image.image_name == image_label.image_name).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        id: str = generate_id(prefix="IMAGE_LABEL")
        new_image_label: ImageLabel = ImageLabel(
            id=id,
            prompt=image_label.prompt,
            tags=image_label.tags,
            gender=image_label.gender,
            image_id=image.id
        )
        image.status = "labelled"
        image.label = new_image_label
        session.commit()
        session.refresh(new_image_label)
        return new_image_label
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
def update_image_label(image_label_id: str, image_label: ImageLabelUpdate, session: Session) -> ImageLabel:
    try:
        logging.info(f"Updating image label with id: {image_label_id}")
        image_label_to_update: ImageLabel = session.query(ImageLabel).filter(ImageLabel.id == image_label_id).first()
        if not image_label_to_update:
            raise HTTPException(status_code=404, detail="Image label not found")
        if image_label.prompt:
            image_label_to_update.prompt = image_label.prompt
        if image_label.tags:
            image_label_to_update.tags = ','.join(image_label.tags)
        if image_label.gender:
            image_label_to_update.gender = image_label.gender
        session.commit()
        session.refresh(image_label_to_update)
        return image_label_to_update
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
def delete_image_label(image_label_id: str, session: Session) -> None:
    try:
        logging.info(f"Deleting image label with id: {image_label_id}")
        session.query(ImageLabel).filter(ImageLabel.id == image_label_id).delete()
        session.commit()
        logging.info(f"Deleted image label with id: {image_label_id}")
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
def get_image_label(image_label_id: str, session: Session) -> ImageLabel | None:
    try:
        image_label: ImageLabel = session.query(ImageLabel).filter(ImageLabel.id == image_label_id).first()
        if not image_label:
            raise HTTPException(status_code=404, detail="Image label not found")
        return image_label
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
def get_all_image_labels(limit: int, offset: int, session: Session) -> list[ImageLabel]:
    try:
        if limit and offset:
            image_labels: list[ImageLabel] = session.query(ImageLabel).limit(limit).offset(offset).all()
        else:
            image_labels: list[ImageLabel] = session.query(ImageLabel).all()
        return image_labels
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()