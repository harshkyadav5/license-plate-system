from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
import cv2

from ..ai.yolo import load_yolo, detect_plate
from ..ai.ocr import predict_plate

router = APIRouter()

yolo_model = None


@router.on_event("startup")
def startup_event():
    global yolo_model
    yolo_model = load_yolo()


def crop_plate(image, box):
    h, w = image.shape[:2]
    x1, y1, x2, y2 = map(int, box)

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    return image[y1:y2, x1:x2]


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()

    np_img = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    detections = detect_plate(image, yolo_model)

    if not detections:
        return {"plate_text": "", "confidence": 0.0}

    plate_box = detections[0]["bbox"]
    plate_img = crop_plate(image, plate_box)

    text, confidence = predict_plate(plate_img)

    return {
        "plate_text": text,
        "confidence": confidence
    }
