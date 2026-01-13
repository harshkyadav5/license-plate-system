from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class ParkingLog(Base):
    __tablename__ = "parking_logs"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    predicted_plate = Column(String(32))
    actual_plate = Column(String(32))
    confidence = Column(Float)
    entry_time = Column(TIMESTAMP, server_default=func.now())
    is_edited = Column(Boolean, default=False)
