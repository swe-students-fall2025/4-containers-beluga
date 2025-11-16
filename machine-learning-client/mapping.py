"""A mapping table: gesture label to (mood, emoji)."""

GESTURE_MAP = {
    "Thumbs Up": ("happy", "😄"),
    "Thumbs Down": ("sad", "😞"),
    "Victory": ("relaxed", "😎"),
    "Open Palm": ("neutral", "🙂"),
    "Fist": ("stressed", "😤"),
}


def map_gesture(label: str):
    """
    Convert a gesture label from the model into a (mood, emoji) pair.
    If unknown, return default
    """
    return GESTURE_MAP.get(label, ("unknown", "??"))
