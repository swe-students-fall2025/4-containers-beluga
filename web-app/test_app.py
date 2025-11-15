"""Tests for the Flask web app."""

from unittest.mock import Mock, patch, MagicMock

import pytest
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
