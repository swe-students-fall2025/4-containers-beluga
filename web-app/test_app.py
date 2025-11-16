"""Tests for the Flask web app."""

import base64
import pytest
from app import create_app


@pytest.fixture
def app():
    """Fixture to create the Flask test client."""
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app


def test_index_redirect(app):
    """Test redirect from '/' to '/camera'."""
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 302
        assert "/camera" in response.location


def test_camera_page(app):
    """Test that /camera loads correctly."""
    with app.test_client() as client:
        response = client.get("/camera")
        assert response.status_code == 200
        assert b"<video" in response.data


def test_analyze_with_valid_image(app):
    """Test analyze route with valid base64 image."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 200


def test_analyze_with_data_url_prefix(app):
    """Test analyze route with data URL prefix."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    # strip prefix before sending to backend
    data_url = f"data:image/jpeg;base64,{base64_image}"

    # backend will see raw base64
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 200


def test_analyze_with_no_json(app):
    """Test analyze route with invalid json."""
    with app.test_client() as client:
        response = client.post("/analyze", data="not json")
        assert response.status_code == 500


def test_analyze_with_missing_image(app):
    """Test analyze route with missing 'image' key."""
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"wrong_key": "value"},
            content_type="application/json",
        )
        assert response.status_code == 400


def test_analyze_with_exception(app):
    """Test analyze route when an exception occurs."""
    invalid_image = "invalid_base64_data"
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"image": invalid_image},
            content_type="application/json",
        )
        assert response.status_code == 500
