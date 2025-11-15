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
Need to download python 3.10 and set the python version of virtual environment to 3.10
install mediapipe and opencv, then start virtual environment.
Get into python bash, import analyze_image function, then call it by using any picture you wanna test.

```bash
cd machine-learning-client
pipenv --python 3.10
pipenv install -d
pipenv shell
```
python
from gesture_api import analyze_image
print(analyze_image("picture_name.jpg"))