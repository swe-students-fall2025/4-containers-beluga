import cv2
import mediapipe as mp
import math
import pprint

mp_hands = mp.solutions.hands.Hands(static_image_mode=True)


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


def is_folded(tip, pip):
    """
    Finger is folded if tip.y and pip.y are close (distance small),
    OR tip slightly above pip (your thumbs-up behaves like this).
    """
    return abs(tip.y - pip.y) < 0.12


def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def analyze_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"gesture": "no_image"}

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(img_rgb)

    if not results.multi_hand_landmarks:
        return {"gesture": "no_hand"}

    lm = results.multi_hand_landmarks[0].landmark
    debug_landmarks(lm)

    # Landmarks
    thumb_tip, thumb_mcp = lm[4], lm[2]
    index_tip, index_pip = lm[8], lm[6]
    middle_tip, middle_pip = lm[12], lm[10]
    ring_tip, ring_pip = lm[16], lm[14]
    pinky_tip, pinky_pip = lm[20], lm[18]

    # Finger bending
    index_bent = is_folded(index_tip, index_pip)
    middle_bent = is_folded(middle_tip, middle_pip)
    ring_bent = is_folded(ring_tip, ring_pip)
    pinky_bent = is_folded(pinky_tip, pinky_pip)

    # ================================
    # Vertical Thumb Up / Down
    # ================================
    thumb_up = thumb_tip.y < thumb_mcp.y - 0.05
    thumb_down = thumb_tip.y > thumb_mcp.y + 0.05

    # 👍 THUMBS UP
    if thumb_up and index_bent and middle_bent and ring_bent and pinky_bent:
        return {"gesture": "thumbs_up", "score": 1.0}

    # 👎 THUMBS DOWN
    if thumb_down and index_bent and middle_bent and ring_bent and pinky_bent:
        return {"gesture": "thumbs_down", "score": 1.0}

    # ✋ Open palm (all straight)
    if not index_bent and not middle_bent and not ring_bent and not pinky_bent:
        return {"gesture": "open_palm", "score": 1.0}

    # ✊ Fist (all folded)
    if index_bent and middle_bent and ring_bent and pinky_bent:
        return {"gesture": "fist", "score": 1.0}

    # =====================================================
    # ✌️  Victory (index + middle straight, others folded)
    # =====================================================
    index_straight = not index_bent
    middle_straight = not middle_bent

    if index_straight and middle_straight and ring_bent and pinky_bent:
        return {"gesture": "victory", "score": 1.0}

    # =====================================================
    # 👌  OK gesture (thumb-index circle)
    # =====================================================
    thumb_index_dist = distance(thumb_tip, index_tip)

    if thumb_index_dist < 0.08 and middle_straight:
        return {"gesture": "ok", "score": 1.0}

    return {"gesture": "unknown", "score": 0.0}
