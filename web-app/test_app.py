# pylint: disable=redefined-outer-name

"""Tests for the Flask web app."""

import os
import time
from unittest.mock import Mock, patch, MagicMock

import pytest
from app import create_app


@pytest.fixture
def flask_client():
    """Fixture to create the Flask test client."""
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app.test_client()


def test_index_page(flask_client):
    """Test that '/' renders the index page."""
    response = flask_client.get("/")
    assert response.status_code == 200
    assert b"Beluga" in response.data or b"AI-Powered" in response.data


def test_camera_page(flask_client):
    """Test that /camera loads correctly."""
    response = flask_client.get("/camera")
    assert response.status_code == 200
    assert b"<video" in response.data


def test_analyze_with_valid_image(flask_client):
    """Test analyze route with valid base64 image."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    with patch.dict(os.environ, {"CI": "true"}):
        response = flask_client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "gesture" in data


def test_analyze_with_data_url_prefix(flask_client):
    """Test analyze route with data URL prefix."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    # Test in CI mode which validates base64 and returns mock response
    with patch.dict(os.environ, {"CI": "true"}):
        response = flask_client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "gesture" in data


def test_analyze_with_no_json(flask_client):
    """Test analyze route with invalid json."""
    response = flask_client.post("/analyze", data="not json")
    assert response.status_code == 500


def test_analyze_with_missing_image(flask_client):
    """Test analyze route with missing 'image' key."""
    response = flask_client.post(
        "/analyze",
        json={"wrong_key": "value"},
        content_type="application/json",
    )
    assert response.status_code == 400


def test_analyze_with_exception(flask_client):
    """Test analyze route when an exception occurs."""
    invalid_image = "invalid_base64_data"
    response = flask_client.post(
        "/analyze",
        json={"image": invalid_image},
        content_type="application/json",
    )
    assert response.status_code == 500


def test_whiteboard_page(flask_client):
    """Test that /whiteboard loads correctly."""
    response = flask_client.get("/whiteboard")
    assert response.status_code == 200
    assert b"whiteboard" in response.data.lower() or b"mood" in response.data.lower()


def test_whiteboard_api_no_db(flask_client):
    """Test /api/whiteboard when database connection fails."""
    with patch("app.get_mongo_collection", return_value=None):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 503
        data = response.get_json()
        assert "error" in data
        assert data["count"] == 0
        assert data["gestures"] == []


def test_whiteboard_api_with_data(flask_client):
    """Test /api/whiteboard with mock database data."""
    # Create mock collection with recent gestures
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "😄",
            "mood": "happy",
            "timestamp": current_time - 3600,  # 1 hour ago
        },
        {
            "gesture": "thumbs_down",
            "emoji": "😞",
            "mood": "sad",
            "timestamp": current_time - 7200,  # 2 hours ago
        },
        {
            "gesture": "victory",
            "emoji": "😎",
            "mood": "excited",
            "timestamp": current_time - 1800,  # 30 minutes ago
        },
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        assert "gestures" in data
        assert "count" in data
        assert data["count"] == 3
        assert len(data["gestures"]) == 3


def test_whiteboard_api_filters_no_hand(flask_client):
    """Test /api/whiteboard filters out no_hand, unknown, and no_image gestures."""
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "😄",
            "mood": "happy",
            "timestamp": current_time - 3600,
        },
        {
            "gesture": "no_hand",
            "emoji": "❓",
            "mood": "unknown",
            "timestamp": current_time - 7200,
        },
        {
            "gesture": "unknown",
            "emoji": "❓",
            "mood": "unknown",
            "timestamp": current_time - 1800,
        },
        {
            "gesture": "no_image",
            "emoji": "❓",
            "mood": "unknown",
            "timestamp": current_time - 900,
        },
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 1
        assert len(data["gestures"]) == 1
        assert data["gestures"][0]["gesture"] == "thumbs_up"


def test_whiteboard_api_exception(flask_client):
    """Test /api/whiteboard when an exception occurs."""
    with patch("app.get_mongo_collection", side_effect=Exception("Database error")):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_analyze_with_ml_server_unknown_gesture(flask_client):
    """Test analyze route with unknown gesture from ML server."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    mock_response = Mock()
    mock_response.json.return_value = {"gesture": "unknown_gesture"}

    with patch.dict(os.environ, {"CI": ""}):
        with patch("app.requests.post", return_value=mock_response):
            response = flask_client.post(
                "/analyze",
                json={"image": base64_image},
                content_type="application/json",
            )
            assert response.status_code == 200
            data = response.get_json()
            assert data["gesture"] == "unknown_gesture"
            assert data["emoji"] == "❓"


def test_format_time_ago_just_now(flask_client):
    """Test _format_time_ago function for recent timestamps."""
    # Test by calling the whiteboard API with a very recent timestamp
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "😄",
            "mood": "happy",
            "timestamp": current_time - 30,  # 30 seconds ago
        }
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        if data["gestures"]:
            assert "just now" in data["gestures"][0]["time_ago"]


def test_format_time_ago_minutes(flask_client):
    """Test _format_time_ago function for minutes."""
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "😄",
            "mood": "happy",
            "timestamp": current_time - 1800,  # 30 minutes ago
        }
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        if data["gestures"]:
            assert "m ago" in data["gestures"][0]["time_ago"]


def test_format_time_ago_hours(flask_client):
    """Test _format_time_ago function for hours."""
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "😄",
            "mood": "happy",
            "timestamp": current_time - 7200,  # 2 hours ago
        }
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        if data["gestures"]:
            assert "h ago" in data["gestures"][0]["time_ago"]


def test_whiteboard_api_empty_when_no_recent_gestures(flask_client):
    """Test /api/whiteboard returns empty when no gestures in last 24 hours."""
    # Mock collection returns empty list (all gestures are older than 24h)
    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = []
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 0
        assert len(data["gestures"]) == 0


def test_whiteboard_api_uses_emoji_from_db(flask_client):
    """Test that /api/whiteboard uses emoji from database if available."""
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "thumbs_up",
            "emoji": "👍",
            "mood": "happy",
            "timestamp": current_time - 3600,
        }
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        assert data["gestures"][0]["emoji"] == "👍"


def test_whiteboard_api_maps_gesture_to_emoji(flask_client):
    """Test that /api/whiteboard maps gestures to emojis when not in DB."""
    current_time = time.time()
    mock_gestures = [
        {
            "gesture": "ok",
            "mood": "content",
            "timestamp": current_time - 3600,
        }
    ]

    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = mock_gestures
    mock_collection.delete_many.return_value = None

    with patch("app.get_mongo_collection", return_value=mock_collection):
        response = flask_client.get("/api/whiteboard")
        assert response.status_code == 200
        data = response.get_json()
        assert data["gestures"][0]["emoji"] == "😊"


def test_analyze_ci_mode_invalid_base64(flask_client):
    """Test analyze route in CI mode with invalid base64."""
    with patch.dict(os.environ, {"CI": "true"}):
        response = flask_client.post(
            "/analyze",
            json={"image": "invalid_base64!!!"},
            content_type="application/json",
        )
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_analyze_different_gesture_types(flask_client):
    """Test analyze route with different gesture types from ML server."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    gesture_types = [
        "thumbs_down",
        "open_palm",
        "fist",
        "victory",
        "rock",
        "ok",
        "point",
    ]

    for gesture_type in gesture_types:
        mock_response = Mock()
        mock_response.json.return_value = {"gesture": gesture_type}

        with patch.dict(os.environ, {"CI": ""}):
            with patch("app.requests.post", return_value=mock_response):
                response = flask_client.post(
                    "/analyze",
                    json={"image": base64_image},
                    content_type="application/json",
                )
                assert response.status_code == 200
                data = response.get_json()
                assert data["gesture"] == gesture_type
                assert "emoji" in data
