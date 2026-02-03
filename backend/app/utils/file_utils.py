import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ParkingLog
from ..utils.file_utils import save_upload, save_crop

from ultralytics import YOLO
from keras.models import load_model

router = APIRouter()

print("Loading YOLO model...")
yolo_model = YOLO("backend/models/yolov8_plate.pt")

print("Loading OCR inference model...")
ocr_model = load_model("backend/ocr_infer.keras")


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_path = save_upload(file)
    image = cv2.imread(image_path)

    if image is None:
        return {"error": "Invalid image file"}

    results = yolo_model(image)
    detections = results[0].boxes

    if detections is None or len(detections) == 0:
        return {"error": "No license plate detected"}

    box = detections[0].xyxy[0].cpu().numpy().astype(int)
    x1, y1, x2, y2 = box

    plate_img = image[y1:y2, x1:x2]

    if plate_img.size == 0:
        return {"error": "Invalid plate crop"}

    crop_path = save_crop(plate_img)

    plate_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    plate_gray = cv2.resize(plate_gray, (200, 50))
    plate_gray = plate_gray / 255.0
    plate_gray = np.expand_dims(plate_gray, axis=(0, -1))

    preds = ocr_model.predict(plate_gray)

    text = preds["text"][0]
    confidence = float(preds["confidence"][0])

    log = ParkingLog(
        plate_text=text,
        confidence=confidence,
        image_path=image_path,
        crop_path=crop_path
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "id": log.id,
        "plate_text": log.plate_text,
        "confidence": log.confidence,
        "image_path": log.image_path,
        "crop_path": log.crop_path
    }
