from fastapi import Request, status, HTTPException, FastAPI
from fastapi.responses import RedirectResponse
import logging


async def unauthorized(request: Request, exc):
    logging.error(exc)
    response = RedirectResponse(url=request.url_for('get_login_page'), status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

async def rate_limit_exceeded(request: Request, exc):
    logging.error(exc)
    return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")


def register_exception_handlers(app: FastAPI):
    logging.info("Registering exception handlers...")
    app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, unauthorized)