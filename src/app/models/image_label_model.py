from __future__ import annotations

from pydantic import BaseModel
from typing import Literal
from app.db.schema import ImageLabel

class ImageLabelCreate(BaseModel):
    image_name: str
    prompt: str
    tags: str = ""
    gender: str = Literal["male", "female"]


class ImageLabelRead(BaseModel):
    id: str
    image_name: str
    prompt: str
    tags: list[str]
    gender: str

    @classmethod
    def from_orm(cls, image_label: ImageLabel):
        return cls(
            id=image_label.id,
            image_name=image_label.image.image_name,
            prompt=image_label.prompt,
            tags=image_label.tags.split(","),
            gender=image_label.gender
        )
    
class ImageLabelUpdate(BaseModel):
    prompt: str | None = None
    tags: str | None = None
    gender: str | None = None