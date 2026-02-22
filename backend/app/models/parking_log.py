from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

from ..database import Base


class ParkingLog(Base):
    __tablename__ = "parking_logs"

    id = Column(Integer, primary_key=True, index=True)

    predicted_plate = Column(String, nullable=False)
    actual_plate = Column(String, nullable=True)

    confidence = Column(Float, nullable=True)

    status = Column(String, default="IN")

    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)

    image_path = Column(String, nullable=True)
    crop_path = Column(String, nullable=True)

    is_edited = Column(Boolean, default=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)