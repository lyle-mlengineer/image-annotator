import jwt
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status, Cookie

from datetime import datetime, timedelta,timezone
from typing import Annotated
import logging

from app.core.config import config
from app.db.db import get_db
from app.models.user_model import UserRead
from app.db.scripts.user_scripts import get_user_by_email
from app.db.schema import User

def create_access_token(
        data: dict,   
    ) -> str: 
    
    to_encode = data.copy()
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    to_encode.update({"exp": expire})  # Include auth method
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

async def get_current_user(
        session: Annotated[Session, Depends(get_db)],
        access_token: Annotated[str, Cookie()] = None,
        ) -> UserRead | None: 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        logging.info("The access token was not provided")
        raise credentials_exception
    try:
        payload = jwt.decode(access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            logging.error("Email not found in token")
            raise credentials_exception

        try:
            user: User = get_user_by_email(email=email, session=session)
        except HTTPException:
            logging.error("User not found after verifying token")
            raise credentials_exception            

        return UserRead.from_orm(user)

    except InvalidTokenError:
        logging.error("Invalid token")
        raise credentials_exception
    

async def get_current_active_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead | None:
    # if current_user and current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

