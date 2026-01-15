from tensorflow import keras

@keras.utils.register_keras_serializable(package="Custom")
class CTCLossLayer(keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loss_fn = keras.backend.ctc_batch_cost

    def call(self, inputs):
        y_true, y_pred, input_length, label_length = inputs
        loss = self.loss_fn(y_true, y_pred, input_length, label_length)
        self.add_loss(loss)
        return y_pred
