from sqlalchemy.orm import Session

import logging

from app.db.schema import User
from app.models.user_model import UserRead, UserUpdate
from app.db.scripts.user_scripts import (
    get_user, get_user_by_email, get_all_users, update_user, delete_user, create_user, authenticate_user
)
from app.services.user_service_helpers import create_access_token


class UserService:
    def __init__(self, db: Session):
        self._db = db

    def create_user(self, user: User) -> UserRead:
        return UserRead.from_orm(create_user(user=user, session=self._db))
    
    def authenticate_user(self, email: str, password: str) -> bool:
        return authenticate_user(email, password, self._db)
    
    def create_access_token(
            self, 
            data: dict, 
        ) -> str:
        return create_access_token(data=data)
        
    def get_user(self, user_id: str) -> UserRead | None:
        user: User = get_user(user_id=user_id, session=self._db)
        return UserRead.from_orm(user)
    
    def get_user_by_email(self, email: str) -> UserRead | None:
        user: User = get_user_by_email(email=email, session=self._db)
        return UserRead.from_orm(user)
    
    def delete_user(self, user_id: str) -> None:
        return delete_user(user_id=user_id, session=self._db)

    def update_user(self, user_id: str, user_update: UserUpdate) -> UserRead | None:
        user: User = update_user(user_id=user_id, user_update=user_update, session=self._db)
        return UserRead.from_orm(user)
    
    def get_all_users(self, limit: int, offset: int) -> list[UserRead]:
        users: list[User] = get_all_users(limit=limit, offset=offset, session=self._db)
        return [UserRead.from_orm(user) for user in users]