"""ML-client API server for gesture recognition."""

import os
import time
import base64
from flask import Flask, request, jsonify
from pymongo import MongoClient
from gesture_api import analyze_image
from mapping import map_gesture
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "testdb")
COLLECTION_NAME = "gestures"

# Initialize MongoDB client with timeout
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def create_app():
    """Factory for creating Flask app (needed for testing)."""
    app = Flask(__name__)

    @app.route("/analyze-image", methods=["POST"])
    def analyze_image_api():
        """Receive base64 image, run gesture detection, store to MongoDB, return result."""
        try:
            data = request.get_json()
            if not data or "image" not in data:
                return jsonify({"error": "No image provided"}), 400

            image_data = data["image"]

            # If begins with data:image/... strip header
            if image_data.startswith("data:image"):
                image_data = image_data.split(",", 1)[1]

            # Decode base64 → bytes
            try:
                img_bytes = base64.b64decode(image_data)
            except Exception as exc:
                return jsonify({"error": "Invalid base64"}), 500

            # Save to temp file
            temp_path = "ml_temp.jpg"
            with open(temp_path, "wb") as f:
                f.write(img_bytes)

            # Call gesture recognizer
            try:
                result = analyze_image(temp_path)
            except Exception as exc:
                return jsonify({"error": f"gesture_api failure: {exc}"}), 500

            gesture = result.get("gesture", "unknown")
            score = result.get("score", 1.0)

            # Map gesture to mood/emoji
            mood, emoji = map_gesture(gesture)

            # Insert into MongoDB
            collection.insert_one({
                "gesture": gesture,
                "score": score,
                "mood": mood,
                "emoji": emoji,
                "timestamp": time.time(),
            })

            # Return result
            return jsonify({
                "gesture": gesture,
                "emoji": emoji,
                "label": gesture,
                "confidence": score,
                "message": "Processed and stored successfully"
            }), 200

        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=True)
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=True)
