"""Main entry point for the gesture recognition ML client."""

import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv

from gesture_api import analyze_image
from mapping import map_gesture

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "testdb")
COLLECTION_NAME = "gestures"


def main():
    """Continuously reads an image, runs gesture recognition, and writes result to MongoDB."""
    print("Starting Gesture ML client...\n")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Test connection
    client.admin.command("ping")
    print("Connected to MongoDB.")

    while True:
        # Later: load the latest uploaded image from web app.
        # For now: run on a sample placeholder image.
        image_path = "sample_thumbs_up_01.jpg"

        result = analyze_image(image_path)
        gesture = result["gesture"]
        score = result["score"]

        mood, emoji = map_gesture(gesture)

        print(f"Detected: {gesture} ({emoji}), score={score}")

        collection.insert_one(
            {
                "gesture": gesture,
                "score": score,
                "mood": mood,
                "emoji": emoji,
                "timestamp": time.time(),
            }
        )

        # Avoid spamming DB every second — simulate periodic check-in
        time.sleep(3)


if __name__ == "__main__":  # pragma: no cover
    main()
