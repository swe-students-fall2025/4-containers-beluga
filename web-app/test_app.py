"""Tests for the Flask web app."""

from unittest.mock import Mock, patch, MagicMock

import pytest
from bson import ObjectId
from app import create_app


@pytest.fixture(name="collection")
def fixture_collection():
    """Return a mock MongoDB collection."""
    return MagicMock()


@pytest.fixture(name="app")
def fixture_app(collection):
    """Create a Flask app with a mocked MongoDB backend."""
    mock_db = MagicMock()
    mock_db.__getitem__ = Mock(return_value=collection)

    with patch("app.MongoClient") as mock_client:
        mock_client.return_value.__getitem__ = Mock(return_value=mock_db)
        mock_client.return_value.admin.command.return_value = None

        app = create_app()
        app.config["TESTING"] = True
        yield app


def test_index_get(client, collection):
    """GET / should render the entry list."""
    collection.find.return_value = [{"_id": ObjectId(), "text": "test entry"}]

    response = client.get("/")
    assert response.status_code == 200
    assert b"test entry" in response.data


def test_index_post(client, collection):
    """POST / should create a new entry."""
    collection.find.return_value = []

    response = client.post("/", data={"text": "new entry"})
    assert response.status_code == 302
    collection.insert_one.assert_called_once()


def test_delete(client, collection):
    """POST /delete should remove an entry."""
    response = client.post("/delete", data={"id": str(ObjectId())})
    assert response.status_code == 302
    collection.delete_one.assert_called_once()
