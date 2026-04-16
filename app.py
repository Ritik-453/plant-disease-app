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

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    image_path = None

    if request.method == "POST":
        file = request.files["image"]

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        image_path = "/" + filepath

    return render_template_string(HTML, image=image_path)


if __name__ == "__main__":
    app.run(debug=True)