from flask import Flask, request, render_template_string
import os

from services.model_service import ModelService
from services.explain_service import ExplainService
from services.disease_service import DiseaseService

# ---------------- INIT ----------------
model_service = ModelService("model/model.h5")
explain_service = ExplainService(model_service.model)
disease_service = DiseaseService()

class_names = ["Healthy", "Diseased"]

app = Flask(__name__, static_folder=".", static_url_path="")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- HTML ----------------
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

    <label>Select Region:</label>
    <select name="region">
        <option value="Rajasthan">Rajasthan</option>
        <option value="Maharashtra">Maharashtra</option>
    </select><br><br>

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

{% if treatment %}
    <h3>🧾 Treatment:</h3>
    <ul>
    {% for t in treatment %}
        <li>{{ t }}</li>
    {% endfor %}
    </ul>
{% endif %}

{% if heatmap %}
    <h3>🔥 Heatmap:</h3>
    <img src="{{ heatmap }}" width="300">
{% endif %}

</body>
</html>
"""

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    image_path = None
    disease = None
    confidence = None
    heatmap_path = None
    treatment = None

    if request.method == "POST":
        file = request.files["image"]
        region = request.form.get("region", "Rajasthan")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        image_path = "/" + filepath

        # Prediction
        idx, confidence, img_array = model_service.predict(filepath)
        disease = class_names[idx]

        # 🌍 Geo filter
        disease = disease_service.apply_geo_filter(disease, region)

        # 🧾 Treatment
        treatment = disease_service.get_treatment(disease)

        # Grad-CAM
        heatmap = explain_service.generate_heatmap(img_array)

        if heatmap is not None:
            heatmap_path = explain_service.overlay_heatmap(filepath, heatmap)

    confidence_display = round(confidence * 100, 2) if confidence is not None else None

    return render_template_string(
        HTML,
        image=image_path,
        disease=disease,
        confidence=confidence_display,
        heatmap=heatmap_path,
        treatment=treatment
    )


if __name__ == "__main__":
    app.run(debug=True)