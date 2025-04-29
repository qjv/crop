
from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os
from io import BytesIO
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            img = Image.open(file.stream)
            xs, ys = img.size
            cropx, cropy = 26, 26
            cropped = img.crop((cropx, cropy, xs - cropx, ys - cropy))

            filename = f"{uuid.uuid4().hex}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            cropped.save(filepath, "WEBP")

            return render_template("index.html", filename=filename)
    return render_template("index.html", filename=None)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
