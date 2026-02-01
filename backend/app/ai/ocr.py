import os
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model, Model

OCR_MODEL_PATH = os.getenv("OCR_MODEL_PATH", "ocr_infer.keras")

CHAR_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
IMG_W = 200
IMG_H = 50

ocr_model: Model | None = None


def load_ocr():
    global ocr_model
    if ocr_model is not None:
        return

    print("Loading OCR inference model...")

    ocr_model = load_model(OCR_MODEL_PATH, compile=False)

    print("OCR inference model loaded")


def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (IMG_W, IMG_H))
    img = img.astype(np.float32) / 255.0

    img = img.T
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)

    return img


def ctc_decode(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]

    decoded, log_prob = tf.keras.backend.ctc_decode(
        pred,
        input_length=input_len,
        greedy=True
    )

    text = ""
    for idx in decoded[0][0]:
        if idx != -1:
            text += CHAR_LIST[int(idx)]

    confidence = float(np.exp(log_prob[0][0]))
    return text, confidence


def predict_plate(img):
    if ocr_model is None or img is None or img.size == 0:
        return "", 0.0

    processed = preprocess(img)
    pred = ocr_model.predict(processed, verbose=0)
    return ctc_decode(pred)
