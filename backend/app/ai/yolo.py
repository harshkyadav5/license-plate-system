import os
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

yolo_model = None

def load_yolo():
    global yolo_model
    if yolo_model is None:
        model_path = os.getenv("YOLO_MODEL_PATH", "best.pt")
        yolo_model = YOLO(model_path)
    return yolo_model
