from services.model_service import ModelService

model_service = ModelService("model/model.h5")

# dummy labels
class_names = ["Healthy", "Diseased"]

from flask import Flask, request, render_template_string
import os

app = Flask(__name__, static_folder=".", static_url_path="")

# folder to store uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Plant Disease Detection</title>
</head>
<body>

<h1>🌿 Upload Plant Image</h1>

<form method="POST" enctype="multipart/form-data">
    <input type="file" name="image" required><br><br>
    <button type="submit">Upload</button>
</form>

{% if image %}
    <h3>Uploaded Image:</h3>
    <img src="{{ image }}" width="300">
{% endif %}

{% if disease %}
    <h2>Prediction: {{ disease }}</h2>
    <h3>Confidence: {{ confidence }}%</h3>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    image_path = None
    disease = None
    confidence = None

    if request.method == "POST":
        file = request.files["image"]

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        image_path = "/" + filepath

        # 🔥 PREDICTION
        idx, confidence, _ = model_service.predict(filepath)
        disease = class_names[idx]

    return render_template_string(
        HTML,
        image=image_path,
        disease=disease,
        confidence=round(confidence * 100, 2) if confidence else None
    )


if __name__ == "__main__":
    app.run(debug=True)