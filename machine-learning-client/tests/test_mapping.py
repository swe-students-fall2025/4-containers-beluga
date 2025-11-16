"""Tests for the gesture mapping functionality."""

from mapping import GESTURE_MAP, map_gesture


def test_map_gesture_thumbs_up():
    """Test mapping for Thumbs Up gesture."""
    mood, emoji = map_gesture("Thumbs Up")
    assert mood == "happy"
    assert emoji == "😄"


def test_map_gesture_thumbs_down():
    """Test mapping for Thumbs Down gesture."""
    mood, emoji = map_gesture("Thumbs Down")
    assert mood == "sad"
    assert emoji == "😞"


def test_map_gesture_victory():
    """Test mapping for Victory gesture."""
    mood, emoji = map_gesture("Victory")
    assert mood == "relaxed"
    assert emoji == "😎"


def test_map_gesture_open_palm():
    """Test mapping for Open Palm gesture."""
    mood, emoji = map_gesture("Open Palm")
    assert mood == "neutral"
    assert emoji == "🙂"


def test_map_gesture_fist():
    """Test mapping for Fist gesture."""
    mood, emoji = map_gesture("Fist")
    assert mood == "stressed"
    assert emoji == "😤"


def test_map_gesture_unknown():
    """Test mapping for unknown gesture returns default."""
    mood, emoji = map_gesture("unknown gesture")
    assert mood == "unknown"
    assert emoji == "??"


def test_map_gesture_empty_string():
    """Test mapping for empty string returns default."""
    mood, emoji = map_gesture("")
    assert mood == "unknown"
    assert emoji == "??"


def test_map_gesture_case_sensitive():
    """Test that mapping is case sensitive."""
    # Lowercase version should not match
    mood, emoji = map_gesture("thumbs up")
    assert mood == "unknown"
    assert emoji == "??"


def test_gesture_map_completeness():
    """Test that all gestures in GESTURE_MAP can be mapped."""
    for gesture, (expected_mood, expected_emoji) in GESTURE_MAP.items():
        mood, emoji = map_gesture(gesture)
        assert mood == expected_mood
        assert emoji == expected_emoji
