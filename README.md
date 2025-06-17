# 🎸 Real-Time Guitar Tuner (Python + PyQt6)

A real time Guitar Trainer app that Suggests a random note on a specific string, and detects the note play via the default mic, and for correct note, it shows, and suggests the next note
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
git clone https://github.com/TheMayukhG/GuitarTrainer.git .

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
```
# 🎯 Tuning Reference
Standard 6-string guitar tuning:

String	Note	Frequency (Hz)
6	E2	82.41
5	A2	110.00
4	D3	146.83
3	G3	196.00
2	B3	246.94
1	E4	329.63

# 🧪 Tested On
✅ Windows 10 / 11

✅ Ubuntu 22.04

✅ Python 3.10+

✅ Works with built-in mic, external interfaces, basically it takes the default device as the input device

# 💬 Credits
Made by TheMayukhG
Student @ Class 10, CBSE — Kendriya Vidyalaya Bolpur.

# 🪓 Future Plans (Optional)
Auto string detection

Support for alternate tunings (Drop D, Open G, etc.)

Visual waveform/spectrum view

Export pitch data to CSV to track improvement

# ☕ Contributing
This is a solo project, but any kind of improvements is heartily welcome

