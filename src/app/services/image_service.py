from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Cookie

from datetime import datetime, timedelta,timezone
from typing import Annotated
import logging

from app.core.config import config
from app.db.db import get_db

from app.db.schema import Image
from app.models.image_model import ImageCreate, ImageUpdate
from app.db.scripts.image_scripts import (
    get_image, get_image_by_name, get_all_images, create_image, update_image, delete_image, 
    get_unlabelled_image
)


class ImageService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_image(self, image_id: str):
        return get_image(image_id=image_id, session=self.db)

    def get_image_by_name(self, image_name: str):
        return get_image_by_name(image_name=image_name, session=self.db)

    def get_all_images(self, limit: int, offset: int):
        return get_all_images(limit=limit, offset=offset, session=self.db)

    def create_image(self, image: ImageCreate):
        return create_image(image=image, session=self.db)

    def update_image(self, image_id: str, image: ImageUpdate):
        return update_image(image_id=image_id, image=image, session=self.db)

    def delete_image(self, image_id: str):
        return delete_image(image_id=image_id, session=self.db)
    
    def get_unlabelled_image(self):
        return get_unlabelled_image(session=self.db)