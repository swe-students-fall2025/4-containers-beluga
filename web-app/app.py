"""Flask web app providing camera interface and gesture analysis."""

import os
import base64
from flask import Flask, jsonify, request, render_template, redirect
import requests


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Redirect root URL to the camera page."""
        return redirect("/camera")

    @app.route("/camera")
    def camera():
        """Render the camera page."""
        return render_template("camera.html")

    @app.route("/analyze", methods=["POST"])
    def analyze():
        """Analyze the uploaded base64 image and return gesture result."""
        try:
            data = request.get_json(force=True, silent=False)

            if not data or "image" not in data:
                return jsonify({"error": "No image provided"}), 400

            image_b64 = data["image"]

            # CI mock: simulate ML server
            if os.getenv("CI") == "true":
                try:
                    base64.b64decode(image_b64, validate=True)
                except Exception:
                    return jsonify({"error": "Invalid base64"}), 500

                return (
                    jsonify(
                        {
                            "gesture": "thumbs_up",
                            "emoji": "👍",
                            "label": "thumbs_up",
                            "confidence": 1.0,
                            "message": "Processed successfully",
                        }
                    ),
                    200,
                )

            # Real ML server call
            ml_response = requests.post(
                "http://localhost:6000/analyze-image",
                json={"image": image_b64},
                timeout=5,
            )
            result = ml_response.json()
            gesture = result.get("gesture", "unknown")

            emoji_map = {
                "thumbs_up": "👍",
                "thumbs_down": "👎",
                "open_palm": "✋",
                "fist": "✊",
                "victory": "✌️",
                "rock": "🤘",
                "ok": "👌",
                "point": "👉",
                "no_hand": "❓",
                "no_image": "❓",
                "unknown": "❓",
            }

            return (
                jsonify(
                    {
                        "gesture": gesture,
                        "emoji": emoji_map.get(gesture, "❓"),
                        "label": gesture,
                        "confidence": 1.0,
                        "message": "Processed successfully",
                    }
                ),
                200,
            )

        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    return app


if __name__ == "__main__":  # pragma: no cover
    APP = create_app()
    APP.run(host="0.0.0.0", port=5000, debug=True)
