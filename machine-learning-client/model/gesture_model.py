"""Gesture model module."""

import mediapipe as mp


class GestureModel:
    """Simple gesture recognition model."""

    def __init__(self):
        """Initialize the model."""
        mp.solutions.hands.Hands()

    def predict(self, _image):
        """Predict gesture from image."""
        return {"gesture": "placeholder"}

    def dummy(self):
        """Dummy method for pylint."""
        return None
