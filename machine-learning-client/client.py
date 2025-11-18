"""ML-client API server for gesture recognition."""

import os
import base64
from flask import Flask, request, jsonify
from gesture_api import analyze_image
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Factory for creating Flask app (needed for testing)."""
    app = Flask(__name__)

    @app.route("/analyze-image", methods=["POST"])
    def analyze_image_api():
        """Receive base64 image, run gesture detection, return result."""
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
            return jsonify({"gesture": gesture}), 200

        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=True)
