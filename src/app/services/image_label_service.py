from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Cookie

from datetime import datetime, timedelta,timezone
from typing import Annotated
import logging

from app.core.config import config
from app.db.db import get_db

from app.db.schema import Image
from app.models.image_label_model import ImageLabelCreate, ImageLabelUpdate, ImageLabelRead
from app.db.scripts.image_label_scripts import (
    get_image_label, get_all_image_labels, create_image_label, update_image_label, delete_image_label
)

class ImageLabelService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_image_label(self, image_label_id: str):
        return get_image_label(image_label_id=image_label_id, session=self.db)
    
    def get_all_image_labels(self, limit: int, offset: int):
        return get_all_image_labels(limit=limit, offset=offset, session=self.db)
    
    def create_image_label(self, image_label: ImageLabelCreate):
        return create_image_label(image_label=image_label, session=self.db)
    
    def update_image_label(self, image_label_id: str, image_label: ImageLabelUpdate):
        return update_image_label(image_label_id=image_label_id, image_label=image_label, session=self.db)
    
    def delete_image_label(self, image_label_id: str):
        return delete_image_label(image_label_id=image_label_id, session=self.db)