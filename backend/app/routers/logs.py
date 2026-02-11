from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..schemas.logs import PlateCorrectionRequest
from ..database import SessionLocal
from ..models import ParkingLog

router = APIRouter(prefix="/logs", tags=["Logs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_logs(
    plate: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(ParkingLog)

    if plate:
        query = query.filter(ParkingLog.predicted_plate.ilike(f"%{plate}%"))

    if status:
        query = query.filter(ParkingLog.status == status.upper())

    logs = (
        query
        .order_by(ParkingLog.entry_time.desc())
        .limit(limit)
        .all()
    )

    return logs


@router.get("/stats")
def get_parking_stats(db: Session = Depends(get_db)):
    total_entries = db.query(ParkingLog).count()

    total_exits = (
        db.query(ParkingLog)
        .filter(ParkingLog.status == "OUT")
        .count()
    )

    currently_inside = (
        db.query(ParkingLog)
        .filter(ParkingLog.status == "IN")
        .count()
    )

    last_activity = (
        db.query(func.max(ParkingLog.updated_at))
        .scalar()
    )

    return {
        "total_entries": total_entries,
        "total_exits": total_exits,
        "currently_inside": currently_inside,
        "last_activity": last_activity
    }


@router.put("/logs/{log_id}/correct")
def correct_plate(
    log_id: int,
    payload: PlateCorrectionRequest,
    db: Session = Depends(get_db)
):
    log = db.query(ParkingLog).filter(ParkingLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    log.actual_plate = payload.actual_plate.upper()
    log.is_edited = True

    db.commit()
    db.refresh(log)

    return {
        "message": "Plate corrected successfully",
        "log_id": log.id,
        "actual_plate": log.actual_plate
    }


@router.get("/logs/active")
def get_active_vehicles(db: Session = Depends(get_db)):
    active_logs = (
        db.query(ParkingLog)
        .filter(ParkingLog.status == "IN")
        .order_by(ParkingLog.entry_time.desc())
        .all()
    )

    return [
        {
            "id": log.id,
            "plate": log.actual_plate or log.predicted_plate,
            "confidence": log.confidence,
            "entry_time": log.entry_time,
            "image_path": log.image_path,
            "crop_path": log.crop_path,
            "is_edited": log.is_edited
        }
        for log in active_logs
    ]