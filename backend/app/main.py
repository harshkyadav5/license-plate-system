import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import upload
from .database import Base, engine
from .ai.yolo import load_yolo
from .ai.ocr import load_ocr

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

# @app.on_event("startup")
# def startup():
#     print("API started (models load lazily)")
@app.on_event("startup")
def startup():
    load_yolo()
    load_ocr()

MEDIA_DIR = os.getenv("MEDIA_DIR", "media")
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(upload.router)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }