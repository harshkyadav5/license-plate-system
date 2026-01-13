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

@router.post("/upload")
def upload_image(file: UploadFile, db: Session = Depends(get_db)):
    image_path = save_upload(file)
    img = cv2.imread(image_path)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    yolo = load_yolo()
    results = yolo(img)

    if len(results[0].boxes) == 0:
        raise HTTPException(status_code=404, detail="No plate detected")

    box = results[0].boxes[0].xyxy[0].cpu().numpy()
    x1, y1, x2, y2 = map(int, box)
    crop = img[y1:y2, x1:x2]

    crop_path = save_crop(crop)

    plate_text, confidence = predict_plate(crop)

    record = ParkingLog(
        image_path=image_path,
        predicted_plate=plate_text,
        actual_plate=plate_text,
        confidence=confidence,
        is_edited=False
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "image_path": image_path,
        "crop_path": crop_path,
        "predicted_plate": plate_text,
        "confidence": confidence
    }
