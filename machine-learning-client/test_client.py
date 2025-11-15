"""Tests for the machine learning client."""

from unittest.mock import Mock, patch, MagicMock

import pytest
from client import main


def _make_stream(changes):
    """Helper to create a mock change stream from a list of changes."""
    stream = MagicMock()
    stream.__enter__ = Mock(return_value=iter(changes))
    stream.__exit__ = Mock(return_value=None)
    return stream


@pytest.fixture(name="mock_collection")
def fixture_mock_collection():
    """Return a mock MongoDB collection."""
    collection = MagicMock()
    collection.find.return_value = [
        {"_id": "1", "text": "entry1"},
        {"_id": "2", "text": "entry2"},
    ]

    # Empty iterator so for loop won't execute
    collection.watch.return_value = _make_stream([])

    return collection


@pytest.fixture(name="mock_db")
def fixture_mock_db(mock_collection):
    """Return a mock MongoDB database."""
    db = MagicMock()
    db.__getitem__ = Mock(return_value=mock_collection)
    return db


@pytest.fixture(name="mock_client")
def fixture_mock_client(mock_db):
    """Return a mock MongoDB client."""
    client = MagicMock()
    client.__getitem__ = Mock(return_value=mock_db)
    client.admin.command.return_value = None
    return client


def test_main_prints_existing_entries(mock_client, capsys):
    """Test that main function prints existing entries."""
    with patch("client.MongoClient", return_value=mock_client):
        main()
        captured = capsys.readouterr()
        assert "entry1" in captured.out
        assert "entry2" in captured.out


def test_main_handles_add(mock_client, mock_collection, capsys):
    """Test that an insert change is printed as an Add."""
    insert_change = {
        "operationType": "insert",
        "fullDocument": {"_id": "3", "text": "entry3"},
    }

    mock_collection.watch.return_value = _make_stream([insert_change])

    with patch("client.MongoClient", return_value=mock_client):
        main()
        captured = capsys.readouterr()
        assert "Add: entry3" in captured.out


def test_main_handles_delete(mock_client, mock_collection, capsys):
    """Test that a delete change is printed as a Remove using existing entries."""
    delete_change = {"operationType": "delete", "documentKey": {"_id": "1"}}

    mock_collection.watch.return_value = _make_stream([delete_change])

    with patch("client.MongoClient", return_value=mock_client):
        main()
        captured = capsys.readouterr()
        assert "Remove: entry1" in captured.out
