"""Flask web app providing camera interface and gesture analysis."""

import os
import time
import base64
from flask import Flask, jsonify, request, render_template, redirect
from pymongo import MongoClient
import requests
from dotenv import load_dotenv

load_dotenv()

ML_PORT = int(os.getenv("MLCLIENT_PORT", "80"))
ML_HOST = os.getenv("MLCLIENT_HOST", "mlclient")

ML_URL = f"http://{ML_HOST}:{ML_PORT}"


def get_mongo_collection():
    """Get MongoDB collection with proper error handling."""
    try:
        MONGO_URI = os.getenv("CONN_STR", os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
        # Extract database name from connection string if present, otherwise use default
        if "/" in MONGO_URI and "?" not in MONGO_URI.split("/")[-1]:
            # Connection string format: mongodb://host:port/dbname
            DB_NAME = os.getenv("DB_NAME", MONGO_URI.split("/")[-1] if "/" in MONGO_URI else "testdb")
        elif "/" in MONGO_URI and "?" in MONGO_URI:
            # Connection string format: mongodb://host:port/dbname?options
            DB_NAME = os.getenv("DB_NAME", MONGO_URI.split("/")[-1].split("?")[0] if "/" in MONGO_URI else "testdb")
        else:
            DB_NAME = os.getenv("DB_NAME", "testdb")

        COLLECTION_NAME = "gestures"

        # Initialize MongoDB client with connection timeout
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = mongo_client[DB_NAME]
        # Test connection
        mongo_client.admin.command('ping')
        return db[COLLECTION_NAME]
    except Exception as exc:
        # Return None if connection fails - will be handled in routes
        print(f"MongoDB connection error: {exc}")
        return None

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Render landing (index) page instead of redirecting to camera."""
        return render_template("index.html")

    @app.route("/camera")
    def camera():
        """Render the camera page."""
        return render_template("camera.html")

    @app.route("/whiteboard")
    def whiteboard():
        """Render the whiteboard page showing today's moods."""
        return render_template("whiteboard.html")

    @app.route("/api/whiteboard", methods=["GET"])
    def get_whiteboard_data():
        """Fetch gestures from the last 24 hours for the whiteboard."""
        try:
            collection = get_mongo_collection()
            if collection is None:
                return jsonify({
                    "gestures": [],
                    "count": 0,
                    "error": "Database connection failed. Please check MongoDB is running."
                }), 503

            # Calculate timestamp from 24 hours ago
            twenty_four_hours_ago = time.time() - (24 * 60 * 60)

            # Query MongoDB for gestures from last 24 hours
            # First, delete entries older than 24 hours
            collection.delete_many({"timestamp": {"$lt": twenty_four_hours_ago}})

            # Fetch recent gestures
            recent_gestures = list(
                collection.find(
                    {"timestamp": {"$gte": twenty_four_hours_ago}},
                    {"_id": 0}  # Exclude MongoDB _id field
                ).sort("timestamp", -1)  # Sort by most recent first
            )

            # Map gestures to mood emojis (using the same mapping as in database)
            mood_map = {
                "thumbs_up": "😄",
                "thumbs_down": "😞",
                "open_palm": "🙂",
                "fist": "😤",
                "victory": "😎",
                "ok": "😊",
                "point": "👉",
            }

            # Format the gestures for display
            formatted_gestures = []
            for gesture in recent_gestures:
                gesture_type = gesture.get("gesture", "unknown")
                # Skip no_hand and unknown gestures - do nothing
                if gesture_type in ["no_hand", "unknown", "no_image"]:
                    continue
                
                # Use emoji from database if available, otherwise map it
                emoji = gesture.get("emoji") or mood_map.get(gesture_type, "❓")
                formatted_gestures.append({
                    "emoji": emoji,
                    "gesture": gesture_type,
                    "mood": gesture.get("mood", "unknown"),
                    "timestamp": gesture.get("timestamp"),
                    "time_ago": _format_time_ago(gesture.get("timestamp", time.time())),
                })

            return jsonify({
                "gestures": formatted_gestures,
                "count": len(formatted_gestures),
                "message": "Whiteboard data retrieved successfully"
            }), 200

        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    def _format_time_ago(timestamp):
        """Format timestamp as human-readable time ago."""
        seconds_ago = time.time() - timestamp
        if seconds_ago < 60:
            return "just now"
        elif seconds_ago < 3600:
            minutes = int(seconds_ago / 60)
            return f"{minutes}m ago"
        elif seconds_ago < 86400:
            hours = int(seconds_ago / 3600)
            return f"{hours}h ago"
        else:
            return "over 24h ago"

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

            # ML server call
            ml_response = requests.post(
                ML_URL + "/analyze-image",
                json={"image": image_b64},
                timeout=30,  # Increased timeout for image processing
            )
            result = ml_response.json()

            # Check for error
            if "error" in result:
                print("error: " + result["error"])
                return jsonify({"error": result["error"]}), 500


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
    port = int(os.environ.get("WEBAPP_PORT", 5000))
    APP.run(host="0.0.0.0", port=port, debug=True)
