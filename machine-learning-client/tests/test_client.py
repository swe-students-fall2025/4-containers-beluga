# pylint: disable=redefined-outer-name
"""Tests for the ML-client Flask API."""

import pytest
from client import app  # <-- CI can load this once __init__.py is added


@pytest.fixture(name="flask_client")
def fixture_flask_client():
    """Flask test client."""
    return app.test_client()


def test_no_image(flask_client):
    """Calling endpoint without image returns 400."""
    response = flask_client.post("/analyze-image", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_valid_image(flask_client, monkeypatch):
    """Valid image should call gesture_api.analyze_image and return gesture."""

    # 1x1 transparent PNG
    tiny_png = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42"
        "mP8/5+hHgAHggJ/PV5l2AAAAABJRU5ErkJggg=="
    )

    # Fake analyze_image return
    def fake_analyze(_path):
        return {"gesture": "thumbs_up", "score": 1.0}

    monkeypatch.setattr("client.analyze_image", fake_analyze)

    response = flask_client.post("/analyze-image", json={"image": tiny_png})
    assert response.status_code == 200

    data = response.get_json()
    assert data["gesture"] == "thumbs_up"


def test_invalid_base64(flask_client):
    """Invalid base64 should trigger 500 error."""
    response = flask_client.post("/analyze-image", json={"image": "not_base64"})
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
