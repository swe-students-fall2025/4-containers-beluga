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


def test_thumb_up():
    """Thumb tip above MCP → thumb_up."""
    fake_img = MagicMock()

    # Create 21 landmarks
    fake_lm = [MagicMock() for _ in range(21)]
    for lm in fake_lm:
        lm.x = 0.5
        lm.z = 0.0

    # thumb_tip = id=4
    # thumb_mcp = id=2
    fake_lm[4].y = 0.40  # above
    fake_lm[2].y = 0.50  # below

    # Make other fingers "not extended"
    for idx in [6, 10, 14, 18, 8, 12, 16, 20]:
        fake_lm[idx].y = 0.50

    mock_results = MagicMock()
    mock_results.multi_hand_landmarks = [MagicMock(landmark=fake_lm)]

    with patch("gesture_api.cv2.imread", return_value=fake_img):
        with patch("gesture_api.cv2.cvtColor", return_value=fake_img):
            with patch("gesture_api.mp_hands.process", return_value=mock_results):
                result = gesture_api.analyze_image("x")
                assert result["gesture"] == "thumbs_up"
