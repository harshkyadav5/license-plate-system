import os
import uuid
import cv2

UPLOAD_DIR = "media/uploads"
CROP_DIR = "media/crops"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROP_DIR, exist_ok=True)


def save_upload(file):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path


def save_crop(img):
    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(CROP_DIR, filename)

    cv2.imwrite(path, img)

    return path