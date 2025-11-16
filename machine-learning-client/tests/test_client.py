# pylint: disable=redefined-outer-name
"""Tests for the ML-client API server."""

import pytest
from client import create_app


@pytest.fixture
def client():
    """Create Flask test client for ML-client server."""
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()


def test_analyze_image_valid(client):
    """Test analyze-image route with valid base64."""
    # Tiny valid PNG transparent pixel (1x1)
    valid_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
        "2mP8/5+hHgAHggJ/PV5l2AAAAABJRU5ErkJggg=="
    )

    response = client.post(
        "/analyze-image",
        json={"image": valid_b64},
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "gesture" in data
    assert "score" in data


def test_analyze_image_invalid_base64(client):
    """Test invalid base64 triggers error response."""
    invalid_b64 = "this_is_not_base64"

    response = client.post(
        "/analyze-image",
        json={"image": invalid_b64},
        content_type="application/json",
    )

    assert response.status_code == 500


def test_analyze_image_missing_key(client):
    """Test missing 'image' key in request."""
    response = client.post(
        "/analyze-image",
        json={"wrong_key": "oops"},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "error" in response.get_json()
