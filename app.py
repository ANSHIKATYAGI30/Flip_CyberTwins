from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "static", "media")
ALLOWED_EXT = {"wav","mp3","ogg","m4a"}

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
app.config["MEDIA_DIR"] = MEDIA_DIR
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit

def allowed(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXT

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/audios")
def list_audios():
    audios = []
    for fname in sorted(os.listdir(app.config["MEDIA_DIR"])):
        if allowed(fname):
            audios.append({
                "name": fname,
                "url": url_for("media_file", filename=fname)
            })
    return jsonify(audios)

@app.route("/media/<path:filename>")
def media_file(filename):
    return send_from_directory(app.config["MEDIA_DIR"], filename, as_attachment=False)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error":"no file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error":"no filename"}), 400
    if not allowed(f.filename):
        return jsonify({"error":"filetype not allowed"}), 400
    fname = secure_filename(f.filename)
    save_path = os.path.join(app.config["MEDIA_DIR"], fname)
    f.save(save_path)
    return jsonify({"success": True, "name": fname, "url": url_for("media_file", filename=fname)}), 201

# Store scheduled posts in memory
scheduled_posts = []

@app.route("/api/schedule", methods=["POST"])
def schedule_post():
    data = request.json
    text = data.get("text")
    time = data.get("time")

    if not text or not time:
        return jsonify({"status": "error", "message": "Text and time required!"}), 400

    scheduled_posts.append({
        "text": text,
        "time": time,
        "created_at": datetime.datetime.now().isoformat()
    })

    return jsonify({"status": "success", "message": f"Post scheduled for {time}!"})

@app.route("/api/scheduled-posts", methods=["GET"])
def get_posts():
    return jsonify(scheduled_posts)

if __name__ == "__main__":
    app.run(debug=True)
app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    # Run with: python app.py
    app.run(host="0.0.0.0", port=5000, debug=True)
