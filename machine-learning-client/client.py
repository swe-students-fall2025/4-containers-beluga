"""Main entry point for machine learning client."""

import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "testdb")


def main():
    """Main execution loop for the ML client."""
    print("Starting ML client...\n")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    client.admin.command("ping")

    collection = db["test"]
    existing_entries = list(collection.find())
    for entry in existing_entries:
        print(entry["text"])

    # Track text values by _id for deletions
    text_by_id = {str(entry["_id"]): entry["text"] for entry in existing_entries}

    try:
        with collection.watch() as stream:
            for change in stream:
                if change["operationType"] == "insert":
                    document = change["fullDocument"]
                    doc_id = str(document["_id"])
                    text = document["text"]
                    text_by_id[doc_id] = text
                    print(f"Add: {text}")
                elif change["operationType"] == "delete":
                    doc_id = str(change["documentKey"]["_id"])
                    text = text_by_id[doc_id]
                    del text_by_id[doc_id]
                    print(f"Remove: {text}")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":  # pragma: no cover
    main()
