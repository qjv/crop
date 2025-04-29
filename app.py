from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageOps
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
            original = img.copy()  # Save original image
            
            xs, ys = img.size
            cropx, cropy = 26, 26
            cropped = img.crop((cropx, cropy, xs - cropx, ys - cropy))

            # Save images with unique filenames
            original_filename = f"{uuid.uuid4().hex}_original.png"
            cropped_filename = f"{uuid.uuid4().hex}_cropped.png"
            
            original.save(os.path.join(UPLOAD_FOLDER, original_filename))
            cropped.save(os.path.join(UPLOAD_FOLDER, cropped_filename))

            return render_template("index.html", 
                                   original_filename=original_filename, 
                                   cropped_filename=cropped_filename)
    return render_template("index.html", 
                           original_filename=None, 
                           cropped_filename=None, 
                           cropped_with_border_filename=None)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
