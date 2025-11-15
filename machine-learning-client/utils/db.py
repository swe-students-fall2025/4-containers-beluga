"""Database utilities."""

import os
from pymongo import MongoClient


class Database:
    """MongoDB wrapper."""

    def __init__(self):
        """Connect to MongoDB."""
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(uri)

    def get_db(self):
        """Return database."""
        return self.client["testdb"]

    def dummy(self):
        """Dummy method for pylint."""
        pass
