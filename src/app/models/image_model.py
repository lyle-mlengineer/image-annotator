from __future__ import annotations

from pydantic import BaseModel
from app.db.schema import Image
from app.models.image_label_model import ImageLabelRead


class ImageCreate(BaseModel):
    image_name: str
    version: str = "v1"
    status: str = "unlabelled"


class ImageRead(BaseModel):
    id: str
    image_name: str
    version: str
    status: str
    label: ImageLabelRead | None

    @classmethod
    def from_orm(cls, image: Image) -> ImageRead:
        return cls(
            id=image.id, 
            image_name=image.image_name, 
            version=image.version, 
            status=image.status,
            label=ImageLabelRead.from_orm(image.label) if image.label else None
        )
    

class ImageUpdate(BaseModel):
    image_name: str | None = None