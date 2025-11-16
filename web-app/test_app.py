"""Tests for the Flask web app."""

import pytest
from app import create_app


@pytest.fixture
def flask_client():
    """Fixture to create the Flask test client."""
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app.test_client()


def test_index_redirect(flask_client):
    """Test redirect from '/' to '/camera'."""
    response = flask_client.get("/")
    assert response.status_code == 302
    assert "/camera" in response.location


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
    response = flask_client.post(
        "/analyze",
        json={"image": base64_image},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_analyze_with_data_url_prefix(flask_client):
    """Test analyze route with data URL prefix."""
    base64_image = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    response = flask_client.post(
        "/analyze",
        json={"image": base64_image},
        content_type="application/json",
    )
    assert response.status_code == 200


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
