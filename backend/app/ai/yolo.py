from ultralytics import YOLO

yolo_model = None


def load_yolo():
    global yolo_model
    if yolo_model is not None:
        return

    print("Loading YOLO...")
    yolo_model = YOLO("best.pt")
    print("YOLO loaded")


def detect_plate(image):
    """
    Runs YOLO inference and returns bounding boxes
    """
    if yolo_model is None:
        raise RuntimeError("YOLO model not loaded")

    results = yolo_model(image, verbose=False)

    detections = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": conf
            })

    return detections
