"""Main entry point for Flask web app."""

import base64

from flask import Flask, jsonify, request, render_template


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

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
            _image_bytes = base64.b64decode(image_data)

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
