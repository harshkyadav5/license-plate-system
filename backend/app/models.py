from sqlalchemy import (Column, Integer, String, Float, Boolean, TIMESTAMP)
from sqlalchemy.sql import func
from .database import Base

class ParkingLog(Base):
    __tablename__ = "parking_logs"

    id = Column(Integer, primary_key=True, index=True)

    image_path = Column(String, nullable=False)
    crop_path = Column(String, nullable=True)

    predicted_plate = Column(String(32), index=True, nullable=False)
    actual_plate = Column(String(32), nullable=True)
    confidence = Column(Float)

    status = Column(String(3), default="IN")
    entry_time = Column(TIMESTAMP, server_default=func.now())
    exit_time = Column(TIMESTAMP, nullable=True)

    duration_minutes = Column(Float, nullable=True)

    is_edited = Column(Boolean, default=False)

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
