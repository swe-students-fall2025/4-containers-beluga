"""Main entry point for Flask web app."""

import os

from flask import Flask, request, redirect, url_for, render_template
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

    return app


if __name__ == "__main__":  # pragma: no cover
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
