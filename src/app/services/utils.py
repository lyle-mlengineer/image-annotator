from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.db import get_db
from app.services.user_service import UserService
from app.services.image_service import ImageService
from app.services.image_label_service import ImageLabelService


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


def get_image_service(db: Session = Depends(get_db)):
    return ImageService(db)


def get_image_label_service(db: Session = Depends(get_db)):
    return ImageLabelService(db)