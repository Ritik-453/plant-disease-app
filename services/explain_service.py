import tensorflow as tf
import numpy as np
import cv2

class ExplainService:
    def __init__(self, model):
        self.model = model

    def get_last_conv_layer(self):
        for layer in reversed(self.model.layers):
            if "conv" in layer.name:
                return layer.name
        return None

    def generate_heatmap(self, img_array):
        last_conv_layer_name = self.get_last_conv_layer()

        # Safety check (dummy model case)
        if last_conv_layer_name is None:
            return None

        grad_model = tf.keras.models.Model(
            [self.model.inputs],
            [self.model.get_layer(last_conv_layer_name).output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, tf.argmax(predictions[0])]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
        return heatmap.numpy()

    def overlay_heatmap(self, img_path, heatmap):
        img = cv2.imread(img_path)
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        superimposed = heatmap * 0.4 + img

        output_path = img_path.replace("uploads", "uploads/heatmap_")
        cv2.imwrite(output_path, superimposed)

        return "/" + output_path