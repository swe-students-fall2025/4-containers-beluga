# ML Client — Gesture Recognition

This folder contains the **machine learning client** that detects hand gestures using a pretrained Mediapipe model.  
The model outputs 21 hand landmarks, and lightweight rule-based logic classifies gestures.

---

## 🚀 Features
- Uses **pretrained Google Mediapipe Hands**
- No training required (ML inference only)
- Classifies:
  - 👍 thumbs up
  - 👎 thumbs down
  - ✋ open palm
  - ✊ fist
  - ✌️ victory
- Returns JSON result
- Fast, local, Docker-friendly

---

## 📦 Setup (Pipenv)

Requires **Python 3.10**

```bash
cd machine-learning-client
pipenv --python 3.10
pipenv install mediapipe opencv-python
pipenv shell

python
from gesture_api import analyze_image
print(analyze_image("picture_name.jpg"))