import os
import uuid
import cv2

UPLOAD_DIR = "media/uploads"
CROP_DIR = "media/crops"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROP_DIR, exist_ok=True)

def save_upload(file):
    ext = file.filename.split(".")[-1]
    name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path

def save_crop(img):
    name = f"{uuid.uuid4()}.jpg"
    path = os.path.join(CROP_DIR, name)
    cv2.imwrite(path, img)
    return path
