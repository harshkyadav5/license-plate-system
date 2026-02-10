from pydantic import BaseModel

class PlateCorrectionRequest(BaseModel):
    actual_plate: str