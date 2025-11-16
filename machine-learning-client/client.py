"""ML-client API server for gesture recognition."""

from flask import Flask, request, jsonify
import base64
import os

from gesture_api import analyze_image

app = Flask(__name__)


@app.route("/analyze-image", methods=["POST"])
def analyze_image_api():
    """Receive base64 image, run gesture detection, return result."""
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        # strip base64 header if exists
        image_data = data["image"]
        if image_data.startswith("data:image"):
            image_data = image_data.split(",", 1)[1]

        img_bytes = base64.b64decode(image_data)

        temp_path = "ml_temp.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_bytes)

        result = analyze_image(temp_path)
        gesture = result.get("gesture", "unknown")

        return jsonify({"gesture": gesture}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=6000, debug=True)
