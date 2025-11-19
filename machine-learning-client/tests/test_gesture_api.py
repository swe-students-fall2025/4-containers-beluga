"""Tests for gesture_api module gesture recognition logic."""

from unittest.mock import patch, MagicMock
import gesture_api


def test_no_image():
    """cv2.imread returns None → 'no_image' result."""
    with patch("gesture_api.cv2.imread", return_value=None):
        result = gesture_api.analyze_image("any.jpg")
        assert result["gesture"] == "no_image"


def test_no_hand():
    """mediapipe finds no hand → 'no_hand' result."""
    fake_img = MagicMock()

    with patch("gesture_api.cv2.imread", return_value=fake_img):
        with patch("gesture_api.cv2.cvtColor", return_value=fake_img):
            with patch(
                "gesture_api.mp_hands.process",
                return_value=MagicMock(multi_hand_landmarks=None),
            ):
                result = gesture_api.analyze_image("img.jpg")
                assert result["gesture"] == "no_hand"
