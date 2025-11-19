"""Tests for ML client Flask API."""

from unittest.mock import patch
import pytest
from client import create_app


@pytest.fixture
def client_app():
    """Create Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_no_image(client_app):
    """Should return 400 when 'image' field missing."""
    response = client_app.post("/analyze-image", json={})
    assert response.status_code == 400


def test_invalid_base64(client_app):
    """Invalid base64 should return 500."""
    response = client_app.post("/analyze-image", json={"image": "not_base64!!"})
    assert response.status_code == 500


@patch("client.collection.insert_one")
@patch("client.analyze_image")
def test_valid_image(mock_analyze, mock_insert, client_app):
    """Valid base64 and mocked analyze_image should return 200."""
    mock_analyze.return_value = {"gesture": "thumbs_up", "score": 0.9}

    tiny_png = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
        "ASsJTYQAAAAASUVORK5CYII="
    )

    response = client_app.post(
        "/analyze-image",
        json={"image": tiny_png},
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json["gesture"] == "thumbs_up"
    mock_analyze.assert_called_once()
    mock_insert.assert_called_once()


@patch("client.collection.insert_one")
@patch("client.analyze_image")
def test_data_url_prefix(mock_analyze, mock_insert, client_app):
    """Handles 'data:image/jpeg;base64,' prefix correctly."""
    mock_analyze.return_value = {"gesture": "fist", "score": 1.0}

    sample_base64 = (
        "data:image/jpeg;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
        "ASsJTYQAAAAASUVORK5CYII="
    )

    response = client_app.post(
        "/analyze-image",
        json={"image": sample_base64},
    )

    assert response.status_code == 200
    assert response.json["gesture"] == "fist"
    mock_analyze.assert_called_once()
    mock_insert.assert_called_once()
