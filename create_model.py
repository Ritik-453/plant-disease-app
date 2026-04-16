import tensorflow as tf
from tensorflow.keras import layers, models
import os

os.makedirs("model", exist_ok=True)

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.save("model/model.h5")

print("✅ Dummy model created")