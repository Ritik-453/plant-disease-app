import tensorflow as tf
import numpy as np

class ModelService:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def preprocess(self, img_path):
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
        img = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        return np.expand_dims(img, axis=0)

    def predict(self, img_path):
        img = self.preprocess(img_path)
        preds = self.model.predict(img)
        idx = np.argmax(preds)
        confidence = float(np.max(preds))
        return idx, confidence, img