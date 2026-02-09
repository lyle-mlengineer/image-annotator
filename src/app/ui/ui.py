from fastapi import status
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import logging

from app.core.config import config

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

router = APIRouter(
    tags=["User Interface"],)


@router.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_landing_page(request: Request):
    """Load the home page"""
    logging.info("Loading landing page")
    return templates.TemplateResponse(
        "landing_page.html", 
        {
            "request": request,
        }
    )

@router.get('/register', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_register_page(request: Request):
    """Load the register page"""
    logging.info("Loading register page")
    return templates.TemplateResponse(
        "register.html", 
        {
            "request": request,
        }
    )

@router.get('/login', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Load the login page"""
    logging.info("Loading login page")
    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request,
            "title": "Login"
        } 
    )

@router.get('/user_dashboard', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_user_dashboard(request: Request):
    """Load the user dashboard"""
    logging.info("Loading user dashboard")
    return templates.TemplateResponse(
        "user_dashboard.html", 
        {
            "request": request,
            "title": "User Dashboard"
        } 
    )

@router.get('/generate_image', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_generate_image(request: Request):
    """Load the generate image page"""
    logging.info("Loading generate image page")
    return templates.TemplateResponse(
        "generate_image.html", 
        {
            "request": request,
            "title": "Generate Image"
        } 
    )

@router.get('/gallery', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_gallery(request: Request):
    """Load the gallery page"""
    logging.info("Loading gallery page")
    return templates.TemplateResponse(
        "gallery.html", 
        {
            "request": request,
            "title": "Gallery"
        } 
    )

@router.get('/settings', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_settings(request: Request):
    """Load the settings page"""
    logging.info("Loading settings page")
    return templates.TemplateResponse(
        "settings.html", 
        {
            "request": request,
            "title": "Settings"
        } 
    )

@router.get('/profile', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_profile(request: Request):
    """Load the profile page"""
    logging.info("Loading profile page")
    return templates.TemplateResponse(
        "profile.html", 
        {
            "request": request,
            "title": "Profile"
        } 
    )

@router.get('/notifications', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_notifications(request: Request):
    """Load the notifications page"""
    logging.info("Loading notifications page")
    return templates.TemplateResponse(
        "notifications.html", 
        {
            "request": request,
            "title": "Notifications"
        } 
    )