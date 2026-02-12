from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin import Admin
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username})

    return {"access_token": token, "token_type": "bearer"}