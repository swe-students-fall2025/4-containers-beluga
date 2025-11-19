"""A mapping table: gesture label to (mood, emoji)."""

GESTURE_MAP = {
    "thumbs_up": ("happy", "😄"),
    "thumbs_down": ("sad", "😞"),
    "victory": ("relaxed", "😎"),
    "open_palm": ("neutral", "🙂"),
    "fist": ("stressed", "😤"),
    "ok": ("content", "😼"),
    "point": ("curious", "🤔"),
}


def map_gesture(label: str):
    """
    Convert a gesture label from the model into a (mood, emoji) pair.
    If unknown, return default
    """
    return GESTURE_MAP.get(label, ("unknown", "??"))
