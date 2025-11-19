"""
Identify gestures module
"""

import math
import pprint
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands(static_image_mode=True)


# --------------------------
# Utility functions
# --------------------------

"""
    Debug print hand landmarks
"""


def debug_landmarks(lm):
    pprint.pprint(
        {
            "thumb": (lm[4].y, lm[2].y),
            "index": (lm[8].y, lm[6].y),
            "middle": (lm[12].y, lm[10].y),
            "ring": (lm[16].y, lm[14].y),
            "pinky": (lm[20].y, lm[18].y),
        }
    )


def is_extended(tip, pip):
    """Finger is extended if tip is clearly higher (smaller y) than pip."""
    return tip.y < pip.y - 0.04


def is_folded(tip, pip):
    """Finger is folded if tip is not above pip."""
    return tip.y > pip.y - 0.01


def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


# --------------------------
# Gesture Recognition
# --------------------------


def analyze_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"gesture": "no_image"}

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(img_rgb)

    if not results.multi_hand_landmarks:
        return {"gesture": "no_hand"}

    lm = results.multi_hand_landmarks[0].landmark
    # debug_landmarks(lm)

    # Landmarks
    thumb_tip, thumb_mcp = lm[4], lm[2]
    index_tip, index_pip = lm[8], lm[6]
    middle_tip, middle_pip = lm[12], lm[10]
    ring_tip, ring_pip = lm[16], lm[14]
    pinky_tip, pinky_pip = lm[20], lm[18]

    # Finger state
    index_ext = is_extended(index_tip, index_pip)
    middle_ext = is_extended(middle_tip, middle_pip)
    ring_ext = is_extended(ring_tip, ring_pip)
    pinky_ext = is_extended(pinky_tip, pinky_pip)

    index_fld = is_folded(index_tip, index_pip)
    middle_fld = is_folded(middle_tip, middle_pip)
    ring_fld = is_folded(ring_tip, ring_pip)
    pinky_fld = is_folded(pinky_tip, pinky_pip)

    # Thumb (vertical)
    thumb_up = thumb_tip.y < thumb_mcp.y - 0.06
    thumb_down = thumb_tip.y > thumb_mcp.y + 0.06

    # ---------------- Gesture rules ----------------

    # 👍 Thumbs up
    if thumb_up and index_fld and middle_fld and ring_fld and pinky_fld:
        return {"gesture": "thumbs_up"}

    # 👎 Thumbs down
    if thumb_down and index_fld and middle_fld and ring_fld and pinky_fld:
        return {"gesture": "thumbs_down"}

    # ✋ Open palm
    if index_ext and middle_ext and ring_ext and pinky_ext:
        return {"gesture": "open_palm"}

    # ✊ Fist
    if index_fld and middle_fld and ring_fld and pinky_fld:
        return {"gesture": "fist"}

    # ✌️ Victory
    if index_ext and middle_ext and ring_fld and pinky_fld:
        return {"gesture": "victory"}

    # 👉 Point
    if index_ext and middle_fld and ring_fld and pinky_fld:
        return {"gesture": "point"}

    # 👌 OK
    if distance(thumb_tip, index_tip) < 0.05 and middle_ext and ring_ext:
        return {"gesture": "ok"}

    return {"gesture": "unknown"}
