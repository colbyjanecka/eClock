from flask import Flask, request, jsonify, send_from_directory
import os, uuid, json
from image import process_image

# info used by newest image API endpoint
UPLOAD_FOLDER = '/var/www/uploads'
META_FILE = os.path.join(UPLOAD_FOLDER, 'latest.json')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/uploads'
app.config['MAX_CONTENT_LENGTH'] = 55 * 1024 * 1024  # 10 MB

# function used to save latest data
def save_latest_metadata(filename, text):
    data = {"filename": filename, "text": text}
    with open(META_FILE,"w") as f:
        json.dump(data, f)

# function to return latest metada
def load_latest_metadata():
    if not os.path.exists(META_FILE):
        return None
    with open(META_FILE) as f:
        return json.load(f)

@app.route("/api/upload", methods=["POST"])
def upload():
    text = request.form.get("text", "").strip()
    file = request.files.get("photo")

    if not text:
        # return jsonify({"error": "Text is required"}), 400
        text = "n/a"
    if not file:
        return jsonify({"error": "Photo is required"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], name)
    file.save(path)

    # PROCESS UPLOADED IMAG
    new_name = process_image(name, text)
    #return jsonify({"error": process_status}), 400

    save_latest_metadata(new_name, text)
    return jsonify({"ok": True, "filename": name})

@app.route("/api/latest", methods=["GET"])
def latest_metadata():
    data = load_latest_metadata()
    if not data:
        return jsonify({"error": "no image yet"}), 404
    return jsonify(data)

@app.route("/api/latest/image", methods=["GET"])
def latest_image():
    data = load_latest_metadata()
    if not data:
        return jsonify({"error": "no image yet"}), 404
    return send_from_directory(app.config["UPLOAD_FOLDER"], data["filename"])
