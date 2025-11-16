"""Gesture recognition API using MediaPipe."""

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands(static_image_mode=True)
mp_draw = mp.solutions.drawing_utils


def analyze_image(image_path):
    """
    Analyze an image to detect hand gestures.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(img_rgb)
    if not results.multi_hand_landmarks:
        return {"gesture": "no hand detected", "score": 0.0}

    hand = results.multi_hand_landmarks[0]

    # Tips
    thumb_tip = hand.landmark[4]
    index_tip = hand.landmark[8]
    middle_tip = hand.landmark[12]
    ring_tip = hand.landmark[16]
    pinky_tip = hand.landmark[20]

    # Knuckles
    index_knuckle = hand.landmark[5]
    middle_knuckle = hand.landmark[9]
    ring_knuckle = hand.landmark[13]
    pinky_knuckle = hand.landmark[17]

    gesture = "unknown"

    # 1. Thumbs Up
    if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y:
        gesture = "thumbs up"

    # 2. Thumbs Down
    elif thumb_tip.y > index_tip.y and thumb_tip.y > middle_tip.y:
        gesture = "thumbs down"

    # 3. Victory
    elif (
        index_tip.y < index_knuckle.y
        and middle_tip.y < middle_knuckle.y
        and ring_tip.y > ring_knuckle.y
        and pinky_tip.y > pinky_knuckle.y
    ):
        gesture = "victory"

    # 4. Open Palm
    elif (
        index_tip.y < index_knuckle.y
        and middle_tip.y < middle_knuckle.y
        and ring_tip.y < ring_knuckle.y
        and pinky_tip.y < pinky_knuckle.y
    ):
        gesture = "open palm"

    # 5. Fist
    elif (
        index_tip.y > index_knuckle.y
        and middle_tip.y > middle_knuckle.y
        and ring_tip.y > ring_knuckle.y
        and pinky_tip.y > pinky_knuckle.y
    ):
        gesture = "fist"

    return {"gesture": gesture, "score": 1.0}
