from fastapi import status
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import logging

from app.core.config import config
from app.ui.ui_helpers import list_images, get_image
from app.services.utils import ImageService, get_image_service
from app.models.image_model import ImageRead

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

@router.get('/upload', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_upload_page(request: Request):
    """Load the upload page"""
    logging.info("Loading upload page")
    return templates.TemplateResponse(
        "upload.html", 
        {
            "request": request,
            "title": "Upload"
        } 
    )

@router.get('/image/label', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_label_page(request: Request, service: ImageService = Depends(get_image_service)):
    """Load the label page"""
    logging.info("Loading label page")
    image: ImageRead = service.get_unlabelled_image()
    if image:
        image_name = image.image_name
    else:
        image_name = None
    return templates.TemplateResponse(
        "label.html", 
        {
            "request": request,
            "title": "Label",
            "image_name": image_name
        } 
    )

    

@router.get('/image/view/{image_name}', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_view_page(request: Request, image_name: str, service: ImageService = Depends(get_image_service)):
    """Load the view page"""
    logging.info("Loading view page")
    image: ImageRead = service.get_image_by_name(image_name)
    return templates.TemplateResponse(
        "view.html", 
        {
            "request": request,
            "title": "View",
            "image": image,
            "label": image.label
        } 
    )

@router.get('/gallery', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_gallery(request: Request, service: ImageService = Depends(get_image_service)):
    """Load the gallery page"""
    logging.info("Loading gallery page")
    images: list[ImageRead] = service.get_all_images(limit=None, offset=None)
    image_names = [image.image_name for image in images]
    return templates.TemplateResponse(
        "gallery_.html", 
        {
            "request": request,
            "title": "Gallery",
            "images": image_names
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