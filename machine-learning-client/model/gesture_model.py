import random

class GestureModel:
    def __init__(self):
        print("[GestureModel] initialized")

    def predict(self, image=None):
        """
           (TODO: revise this)
           Fake random gesture output
        """
        gestures = ["fist", "palm", "ok", "peace", "rock", "unknown"]
        return random.choice(gestures)
