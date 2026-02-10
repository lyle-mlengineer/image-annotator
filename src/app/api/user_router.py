from fastapi import APIRouter, Request, HTTPException, status, Depends, Form, Cookie
from fastapi.responses import RedirectResponse

import logging
from typing import Annotated, Literal

from app.services.utils import get_user_service, UserService
from app.models.user_model import UserCreate, UserRead
from app.core.config import config


router = APIRouter(
    tags=["User"],
)

@router.post("/register")
async def register(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    service: UserService = Depends(get_user_service)
    ):
    user: UserCreate = UserCreate(
        name=username,
        email=email,
        password=password,
    )
    user: UserRead = service.create_user(user=user)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    # return user

@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    service: UserService = Depends(get_user_service)
    ):
    service.authenticate_user(email=email, password=password) 
    token: str = service.create_access_token(data={"sub": email}) 
    response = RedirectResponse(url="/user_dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token", 
        value=token, 
        httponly=config.HTTP_ONLY, 
        samesite=config.SAMESITE, 
        max_age=config.MAX_AGE
    )
    return response

@router.get("/logout")
async def logout(request: Request):
    logging.info("Logging out...")
    response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    logging.info("Deleting cookie...")
    response.delete_cookie(key="access_token")
    return response