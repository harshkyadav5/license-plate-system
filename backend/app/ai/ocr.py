import os
import cv2
import numpy as np
import tensorflow as tf
from dotenv import load_dotenv
from tensorflow.keras.models import load_model

load_dotenv()

OCR_MODEL_PATH = os.getenv("OCR_MODEL_PATH", "ocr_model.keras")

CHAR_LIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
IMG_W = 200
IMG_H = 50

ocr_model = None

def load_ocr():
    global ocr_model
    if ocr_model is None:
        ocr_model = load_model(OCR_MODEL_PATH, compile=False)
    return ocr_model


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
    model = load_ocr()
    processed = preprocess(img)
    pred = model.predict(processed, verbose=0)
    return ctc_decode(pred)
