"""Tests for the Flask web app."""

import pytest
from app import create_app


@pytest.fixture
def client():
    """Fixture to create the Flask test client."""
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app.test_client()


def test_index_redirect(client):
    """Test redirect from '/' to '/camera'."""
    response = client.get("/")
    assert response.status_code == 302
    assert "/camera" in response.location


def test_camera_page(client):
    """Test that /camera loads correctly."""
    response = client.get("/camera")
    assert response.status_code == 200
    assert b"<video" in response.data


def test_analyze_with_valid_image(client):
    """Test analyze route with valid base64 image."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    response = client.post(
        "/analyze",
        json={"image": base64_image},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_analyze_with_data_url_prefix(client):
    """Test analyze route with data URL prefix."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    response = client.post(
        "/analyze",
        json={"image": base64_image},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_analyze_with_no_json(client):
    """Test analyze route with invalid json."""
    response = client.post("/analyze", data="not json")
    assert response.status_code == 500


def test_analyze_with_missing_image(client):
    """Test analyze route with missing 'image' key."""
    response = client.post(
        "/analyze",
        json={"wrong_key": "value"},
        content_type="application/json",
    )
    assert response.status_code == 400


def test_analyze_with_exception(client):
    """Test analyze route when an exception occurs."""
    invalid_image = "invalid_base64_data"
    response = client.post(
        "/analyze",
        json={"image": invalid_image},
        content_type="application/json",
    )
    assert response.status_code == 500
