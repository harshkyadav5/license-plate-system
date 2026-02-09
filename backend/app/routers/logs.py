from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

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