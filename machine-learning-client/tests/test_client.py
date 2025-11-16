"""Tests for the ML client."""

from unittest.mock import MagicMock, patch

import pytest
from client import main


@pytest.fixture(name="mock_client")
def fixture_mock_client():
    """Fixture to mock MongoDB client."""
    fake_collection = MagicMock()
    fake_collection.insert_one = MagicMock(return_value=None)

    fake_db = MagicMock()
    fake_db.__getitem__ = MagicMock(return_value=fake_collection)

    fake_admin = MagicMock()
    fake_admin.command = MagicMock(return_value=None)

    fake_client = MagicMock()
    fake_client.admin = fake_admin
    fake_client.__getitem__ = MagicMock(return_value=fake_db)

    return fake_client


@pytest.fixture(name="mock_analyze")
def fixture_mock_analyze_image():
    """Fixture to mock analyze_image function."""
    return MagicMock(return_value={"gesture": "thumbs up", "score": 0.95})


def test_main_runs(mock_client, mock_analyze):
    """
    Basic smoke test to ensure main() runs without crashing.
    We mock MongoDB calls so it does not touch real database.
    """
    with (
        patch("client.MongoClient", return_value=mock_client),
        patch("gesture_api.analyze_image", mock_analyze),
        patch("builtins.print"),
        patch("time.sleep", side_effect=KeyboardInterrupt()),
    ):
        with pytest.raises(KeyboardInterrupt):
            main()
