from __future__ import annotations

from pydantic import BaseModel
from app.db.schema import User


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserRead(BaseModel):
    id: str
    name: str
    email: str

    @staticmethod
    def from_orm(user: User) -> UserRead:        
        return UserRead(
            id=user.id,
            name=user.name,
            email=user.email   
        )

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None