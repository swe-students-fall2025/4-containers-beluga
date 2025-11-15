"""Main entry point for Flask web app."""

import base64
import os

from flask import Flask, jsonify, request, redirect, url_for, render_template
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "testdb")


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    client.admin.command("ping")

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Render the form and list existing entries."""
        if request.method == "POST":
            if text := request.form.get("text", "").strip():
                db["test"].insert_one({"text": text})
            return redirect(url_for("index"))

        entries = [
            {"id": str(entry["_id"]), "text": entry["text"]}
            for entry in db["test"].find()
        ]
        return render_template("index.html", entries=entries)

    @app.route("/delete", methods=["POST"])
    def delete():
        """Delete an entry."""
        if entry_id := request.form.get("id", ""):
            db["test"].delete_one({"_id": ObjectId(entry_id)})
        return redirect(url_for("index"))

    @app.route("/camera")
    def camera():
        """Render the camera page."""
        return render_template("camera.html")

    @app.route("/analyze", methods=["POST"])
    def analyze():
        """Analyze an image using the ML client."""
        try:
            data = request.get_json()
            if not data or "image" not in data:
                return jsonify({"error": "No image provided"}), 400

            # Extract base64 image data
            image_data = data["image"]
            if image_data.startswith("data:image"):
                # Remove data URL prefix (e.g., "data:image/jpeg;base64,")
                image_data = image_data.split(",", 1)[1]

            # Decode base64 image
            image_bytes = base64.b64decode(image_data)

            # TODO: Send image to ML client for processing
            # For now, return a placeholder response

            # Placeholder response - replace with actual ML client integration
            response_data = {
                "label": "thumbs_up",  # Placeholder
                "confidence": 0.95,  # Placeholder
                "emoji": "👍",  # Placeholder
                "message": "Image received. ML processing not yet integrated.",
            }

            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":  # pragma: no cover
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
