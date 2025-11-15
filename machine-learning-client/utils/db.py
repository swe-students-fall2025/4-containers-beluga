from pymongo import MongoClient
import os

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
        db_name = os.getenv("DB_NAME", "testdb")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["ml_results"]

        print("[Database] Connected to", mongo_uri)

    def insert_result(self, gesture, source="mediapipe"):
        doc = {
            "gesture": gesture,
            "source": source
        }
        self.collection.insert_one(doc)
        print("[Database] Inserted", doc)