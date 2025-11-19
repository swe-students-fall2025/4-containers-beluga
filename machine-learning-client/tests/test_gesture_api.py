from unittest.mock import patch, MagicMock
import gesture_api


def test_no_image():
    """When cv2.imread returns None → no_image."""
    with patch("gesture_api.cv2.imread", return_value=None):
        result = gesture_api.analyze_image("any.jpg")
        assert result["gesture"] == "no_image"
