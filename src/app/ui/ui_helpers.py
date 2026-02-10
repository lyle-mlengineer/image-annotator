from app.core.config import config
import os
import random


def list_images():
    images: list[str] = os.listdir(config.DATA_DIR)
    return images

def get_image():
    images: list[str] = list_images()
    return random.choice(images)