from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import numpy as np
import cv2
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..ai.yolo import load_yolo, detect_plate
from ..ai.ocr import predict_plate
from ..database import SessionLocal
from ..models import ParkingLog
from ..utils.file_utils import save_upload, save_crop

router = APIRouter()

yolo_model = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    np_img = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    image_path = save_upload(file)

    detections = detect_plate(image, yolo_model)
    if not detections:
        return {"error": "No license plate detected"}

    plate_box = detections[0]["bbox"]
    plate_img = crop_plate(image, plate_box)

    crop_path = save_crop(plate_img)

    plate_text, confidence = predict_plate(plate_img)
    if not plate_text:
        return {"error": "OCR failed"}

    last_log = (
        db.query(ParkingLog)
        .filter(ParkingLog.predicted_plate == plate_text)
        .order_by(ParkingLog.entry_time.desc())
        .first()
    )

    if last_log and last_log.status == "IN":
        last_log.status = "OUT"
        last_log.exit_time = func.now()
        last_log.confidence = confidence
        db.commit()

        return {
            "plate": plate_text,
            "status": "EXIT",
            "confidence": confidence
        }

    else:
        new_log = ParkingLog(
            image_path=image_path,
            crop_path=crop_path,
            predicted_plate=plate_text,
            confidence=confidence,
            status="IN"
        )

        db.add(new_log)
        db.commit()

        return {
            "plate": plate_text,
            "status": "ENTRY",
            "confidence": confidence
        }
