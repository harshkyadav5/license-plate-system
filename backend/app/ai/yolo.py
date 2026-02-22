from ultralytics import YOLO

yolo_model = None


def load_yolo():
    global yolo_model
    if yolo_model is None:
        print("Loading YOLO model...")
        yolo_model = YOLO("best.pt")
    return yolo_model


def detect_plate(image):
    global yolo_model
    if yolo_model is None:
        raise RuntimeError("YOLO model not loaded")

    results = yolo_model(image, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            detections.append({"bbox": [x1, y1, x2, y2], "confidence": conf})

    return detections