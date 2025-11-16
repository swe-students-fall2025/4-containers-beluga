"""Tests for ML-client analyze-image API."""

import pytest
from client import app


@pytest.fixture(name="client")
def fixture_client():
    """Flask test client."""
    return app.test_client()


def test_analyze_missing_image(client):
    """Should return 400 when no image is provided."""
    response = client.post("/analyze-image", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_analyze_invalid_base64(client):
    """Should return 500 when base64 cannot be decoded."""
    invalid_b64 = "not_valid_base64!!!"
    response = client.post("/analyze-image", json={"image": invalid_b64})
    assert response.status_code == 500
    assert "error" in response.get_json()


def test_analyze_valid_minimal_png(client):
    """Should return gesture result for tiny valid base64 image."""

    # Tiny valid 1×1 transparent PNG
    valid_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mP8/5+hHgAHggJ/PV5l2AAAAABJRU5ErkJggg=="
    )

    response = client.post(
        "/analyze-image",
        json={"image": valid_b64},
        content_type="application/json",
    )

    assert response.status_code == 200

    data = response.get_json()
    assert "gesture" in data
