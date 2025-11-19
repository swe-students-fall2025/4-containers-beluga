import base64
import pytest
from unittest.mock import patch, MagicMock
from client import create_app


@pytest.fixture
def flask_client():
    """Create Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_no_image(flask_client):
    """Return 400 when 'image' field missing."""
    response = flask_client.post("/analyze-image", json={})
    assert response.status_code == 400


def test_invalid_base64(flask_client):
    """Invalid base64 should return 500."""
    response = flask_client.post("/analyze-image", json={"image": "not_base64"})
    assert response.status_code == 500


@patch("client.collection.insert_one")
@patch("client.analyze_image")
def test_valid_image(mock_analyze, mock_insert, flask_client):
    """Valid base64 and mocked analyze_image should return 200."""
    # Mock analyze_image response
    mock_analyze.return_value = {"gesture": "thumbs_up", "score": 0.9}

    # Real tiny 1x1 png base64
    tiny_png = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
        "ASsJTYQAAAAASUVORK5CYII="
    )

    response = flask_client.post(
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
def test_data_url_prefix(mock_analyze, mock_insert, flask_client):
    """Handles 'data:image/jpeg;base64,' prefix correctly."""
    mock_analyze.return_value = {"gesture": "fist", "score": 1.0}

    sample_base64 = (
        "data:image/jpeg;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
        "ASsJTYQAAAAASUVORK5CYII="
    )

    response = flask_client.post("/analyze-image", json={"image": sample_base64})

    assert response.status_code == 200
    assert response.json["gesture"] == "fist"

    mock_analyze.assert_called_once()
    mock_insert.assert_called_once()
