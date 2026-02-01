import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import load_model, Model

class CTCLossLayer(layers.Layer):
    def call(self, inputs):
        y_pred, labels, input_length, label_length = inputs
        loss = tf.keras.backend.ctc_batch_cost(
            labels, y_pred, input_length, label_length
        )
        self.add_loss(loss)
        return y_pred


TRAIN_MODEL_PATH = "backend/ocr_model.keras"
EXPORT_MODEL_PATH = "backend/ocr_infer.keras"

print("Loading training OCR model...")

training_model = load_model(
    TRAIN_MODEL_PATH,
    compile=False,
    custom_objects={"CTCLossLayer": CTCLossLayer},
)

print("Building inference model...")

infer_model = Model(
    inputs=training_model.input,
    outputs=training_model.get_layer("dense_2").output
)

infer_model.save(EXPORT_MODEL_PATH)

print(f"OCR inference model exported: {EXPORT_MODEL_PATH}")
