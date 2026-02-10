# filepath: main.py
import aiofiles
import os
import uuid
from fastapi import File, UploadFile, HTTPException, APIRouter, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import logging

from app.core.config import config

router = APIRouter(
    tags=["Images"],
)

class LabelRequest(BaseModel):
    image_name: str
    prompt: str
    tags: list[str]
    gender: str


@router.post("/upload")
async def upload_simple(
    request: Request,
    file: UploadFile = File(...),
    ):
    """
    Saves a file to the upload directory with a secure, unique filename.
    """
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=415, detail="Unsupported file type.")

    # Generate a secure, unique filename to prevent path traversal and overwrites
    file_extension = os.path.splitext(file.filename)[1]
    secure_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(config.DATA_DIR, secure_filename)
    file_url: str = request.url_for("data", path=secure_filename)

    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # Read file content
            await out_file.write(content)  # Write to disk
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    finally:
        # Ensure the temporary file is closed
        await file.close()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "stored_at": file_path,
        "url": file_url.__str__(),
    }

@router.post("/label", status_code=status.HTTP_200_OK)
async def get_label_page(
    request: Request,
    label_request: LabelRequest
    ):
    """Load the label page"""
    return label_request
    
