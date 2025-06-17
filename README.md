# 🎸 Real-Time Guitar Tuner (Python + PyQt6)

A real-time guitar tuning app that uses live microphone input to detect pitch, calculate accuracy in cents/semitones, and display it with a slick PyQt6 interface.

Built using:
- 🎤 Live audio capture via `sounddevice`
- 🎶 Pitch detection using `librosa` (YIN algorithm)
- 💻 GUI made with `PyQt6`
- 🧠 Math handled by `numpy`

---

## 🚀 Features

- Detects pitch in real-time from your guitar
- Compares played note to standard tuning
- Shows tuning accuracy in **semitones and cents**
- Clean and responsive UI
- Modular and hackable codebase (good for tinkerers)

---

## 📦 Requirements

- Python 3.8+
- See `requirements.txt` for full list:
  - `numpy`
  - `librosa`
  - `sounddevice`
  - `PyQt6`

---

## 🛠️ Setup (Clone-and-Go)

```bash
# Step 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/guitar-tuner.git
cd guitar-tuner

# Step 2: Create a virtual environment
python -m venv venv

# Step 3: Activate the environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Run the app
python main.py
