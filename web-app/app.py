"""Main entry point for Flask web app."""

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
        try:
            # Parse JSON
            data = request.get_json(force=True, silent=False)

            # Missing or empty JSON
            if not data or "image" not in data:
                return jsonify({"error": "No image provided"}), 400

            image_b64 = data["image"]

            # call the ML-client API
            ml_response = requests.post(
                "http://localhost:6000/analyze-image",
                json={"image": image_b64},
                timeout=5,
            )

            gesture = ml_response.json().get("gesture", "unknown")

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
                    "message": "Processed successfully",
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":  # pragma: no cover
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
