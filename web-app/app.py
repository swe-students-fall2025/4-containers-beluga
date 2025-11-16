"""Main entry point for Flask web app."""

import base64

from flask import Flask, jsonify, request, render_template, redirect
import requests


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return redirect("/camera")

    @app.route("/camera")
    def camera():
        """Render the camera page."""
        return render_template("camera.html")

    @app.route("/analyze", methods=["POST"])
    def analyze():
        data = request.get_json()

        # call the ML-client API
        ml_response = requests.post(
            "http://localhost:6000/analyze-image", json={"image": data["image"]}
        )

        gesture = ml_response.json().get("gesture", "unknown")

        # FULL gesture → emoji mapping table
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

        return jsonify(
            {
                "gesture": gesture,
                "emoji": emoji_map.get(gesture, "❓"),
                "label": gesture,
                "confidence": 1.0,
            }
        )

    return app


if __name__ == "__main__":  # pragma: no cover
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
