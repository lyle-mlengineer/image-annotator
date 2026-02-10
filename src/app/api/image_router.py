# filepath: main.py
import aiofiles
import os
import uuid
from fastapi import File, UploadFile, HTTPException, APIRouter, Request, status, Depends
from pydantic import BaseModel

import logging

from app.core.config import config
from app.services.utils import (
    get_image_service, ImageService, get_image_label_service, ImageLabelService
)
from app.models.image_model import ImageRead, ImageCreate
from app.models.image_label_model import ImageLabelCreate, ImageLabelRead, ImageLabelUpdate

router = APIRouter(
    tags=["Images"],
)

class LabelRequest(BaseModel):
    image_name: str
    prompt: str
    tags: list[str]
    gender: str


@router.post("/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    service: ImageService = Depends(get_image_service)
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

    try:
        image = ImageCreate(
            image_name=secure_filename,
        )
        service.create_image(image)
    except Exception as e:
        logging.error(f"Error creating image: {e}")
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    return {
        "filename": secure_filename,
        "content_type": file.content_type,
        "stored_at": file_path,
        "url": file_url.__str__(),
    }

@router.post("/label", status_code=status.HTTP_200_OK)
async def label_image(
    request: Request,
    label_request: LabelRequest,
    service: ImageLabelService = Depends(get_image_label_service)
    ):
    """Load the label page"""
    logging.info("Labeling image")
    print(label_request.tags)
    label: ImageLabelRead = service.create_image_label(
        image_label=ImageLabelCreate(
            image_name=label_request.image_name,
            prompt=label_request.prompt,
            tags=','.join(label_request.tags),
            gender=label_request.gender
        )
    )
    return label
    
