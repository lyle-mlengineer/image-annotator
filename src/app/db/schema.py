from __future__ import annotations

from sqlalchemy import String, DateTime, ForeignKey, Float, Text, Integer, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.core.extensions import password_hash 
from app.core.config import config


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return password_hash.hash(password)

class Image(Base):
    __tablename__ = "images"

    id: Mapped[str] = mapped_column(primary_key=True)
    image_name: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String, default="v1")
    status: Mapped[str] = mapped_column(String, default="unlabelled")

    label: Mapped[ImageLabel] = relationship("ImageLabel", back_populates="image", uselist=False)

class ImageLabel(Base):
    __tablename__ = "image_labels"

    id: Mapped[str] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(String)
    tags: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    image_id: Mapped[str] = mapped_column(ForeignKey("images.id"))

    image: Mapped[Image] = relationship("Image", back_populates="label", uselist=False)