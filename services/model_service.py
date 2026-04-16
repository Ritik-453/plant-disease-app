import tensorflow as tf
import numpy as np
import os

class ModelService:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model = tf.keras.models.load_model(model_path)

    def preprocess(self, img_path):
        IMG_SIZE = 224
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
        img = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        return np.expand_dims(img, axis=0)

    def predict(self, img_path):
        img = self.preprocess(img_path)
        preds = self.model.predict(img, verbose=0)

        idx = np.argmax(preds)
        confidence = float(np.max(preds))

        return idx, confidence, img