from keras.models import load_model, Model
from keras.saving import register_keras_serializable
from keras import layers

@register_keras_serializable()
class CTCLossLayer(layers.Layer):
    def call(self, inputs):
        return inputs

print("Loading OCR training model...")

training_model = load_model(
    "backend/ocr_model.keras",
    compile=False,
    custom_objects={
        "CTCLossLayer": CTCLossLayer
    }
)

print("Building inference model...")

y_pred = training_model.layers[-2].output

infer_model = Model(
    inputs=training_model.inputs[0],
    outputs=y_pred
)

infer_model.save("backend/ocr_infer.keras")
print("Saved backend/ocr_infer.keras")
