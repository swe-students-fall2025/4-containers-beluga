"""Tests for the Flask web app."""

import pytest
from app import create_app


@pytest.fixture(name="app")
def fixture_app():
    """Create a Flask app for testing."""
    app = create_app()
    app.config["TESTING"] = True
    yield app


def test_camera_route(app):
    """Test GET request to camera route."""
    with app.test_client() as client:
        response = client.get("/camera")
        assert response.status_code == 200


def test_analyze_with_valid_image(app):
    """Test analyze route with valid base64 image."""
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "label" in data
        assert "confidence" in data
        assert "emoji" in data
        assert "message" in data


def test_analyze_with_data_url_prefix(app):
    """Test analyze route with data URL prefix."""
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
    data_url = f"data:image/jpeg;base64,{base64_image}"
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"image": data_url},
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "label" in data


def test_analyze_without_image(app):
    """Test analyze route without image."""
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={},
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No image provided"


def test_analyze_with_missing_image_key(app):
    """Test analyze route with missing image key."""
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            json={"other": "data"},
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No image provided"


def test_analyze_with_invalid_json(app):
    """Test analyze route with invalid JSON."""
    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data="invalid json",
            content_type="application/json",
        )
        # Invalid JSON triggers an exception, which returns 500
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_analyze_with_exception(app):
    """Test analyze route when an exception occurs."""
    base64_image = "invalid_base64_data_that_will_cause_error"
    with app.test_client() as client:
        # This should trigger an exception in base64 decoding
        response = client.post(
            "/analyze",
            json={"image": base64_image},
            content_type="application/json",
        )
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
