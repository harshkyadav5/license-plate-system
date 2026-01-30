from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import cv2

from ..database import SessionLocal
from ..models import ParkingLog
from ..ai.yolo import load_yolo
from ..ai.ocr import predict_plate
from ..utils.file_utils import save_upload, save_crop

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

    detections = detect_plate(image)

    if not detections:
        return {"error": "No license plate detected"}

    plate_box = detections[0]["bbox"]

    plate_img = crop_plate(image, plate_box)

    text, confidence = predict_plate(plate_img)

    return {
        "plate_text": text,
        "confidence": confidence
    }
