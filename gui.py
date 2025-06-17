from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QFileSystemWatcher, pyqtSignal, QTimer
from PyQt6.QtGui import QFontDatabase

from constants import STANDARD_TUNING
from tuner_utils import get_pitch_difference, freq_to_note_name, is_pitch_close
from audio_stream import AudioPitchStream
import random


def load_custom_fonts():
    paths = [
        "assets/fonts/Poppins-Regular.ttf",
        "assets/fonts/Poppins-Bold.ttf"
    ]
    for path in paths:
        font_id = QFontDatabase.addApplicationFont(path)
        if font_id == -1:
            print(f"Failed to load font: {path}")
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            print(f"Loaded font: {families}")


class GuitarTrainer(QWidget):
    pitch_received = pyqtSignal(float, float)  # (frequency, confidence)

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 340)
        self.setWindowTitle("🎸 Guitar Trainer")
        self.setGeometry(200, 200, 400, 300)

        self.last_freq = None
        self.last_note = ""
        self.same_count = 0

        self.selected_string = "E2"
        self.target_freq = STANDARD_TUNING[self.selected_string]
        self.target_note = "E2"
        self.target_fret = 0

        self.pitch_received.connect(self.process_audio)

        self.setup_ui()
        self.set_next_target()
        self.setup_styles("style.qss")

        self.audio_stream = AudioPitchStream(self.pitch_received.emit)
        self.audio_stream.start()

        # Optional: keep-alive debug
        self.keep_alive = QTimer()
        self.keep_alive.timeout.connect(lambda: print("."))
        self.keep_alive.start(5000)

        self.show()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        string_row = QHBoxLayout()
        string_row.setSpacing(6)
        self.string_buttons = {}

        for string_name in STANDARD_TUNING.keys():
            btn = QPushButton(string_name)
            btn.setObjectName("stringButton")
            btn.setFixedSize(40, 32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, s=string_name: self.change_string(s))
            self.string_buttons[string_name] = btn
            string_row.addWidget(btn)

        layout.addLayout(string_row)

        self.note_label = QLabel(self.target_note)
        self.note_label.setObjectName("noteLabel")
        self.note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(QLabel("Play this note", alignment=Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.note_label)

        self.result_label = QLabel("")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        self.debug_label = QLabel("")
        self.debug_label.setObjectName("debugLabel")
        self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.debug_label)

        self.setLayout(layout)

    def change_string(self, string_name):
        self.selected_string = string_name
        self.set_next_target()
        self.result_label.setText("")
        self.debug_label.setText("")

    def set_next_target(self):
        self.target_fret = random.randint(0, 12)
        base_freq = STANDARD_TUNING[self.selected_string]
        self.target_freq = base_freq * (2 ** (self.target_fret / 12))
        self.target_note, _ = freq_to_note_name(self.target_freq)
        self.note_label.setText(f"{self.target_note}")

    def process_audio(self, freq, conf):
        if freq <= 0:
            self.result_label.setText("No pitch detected")
            self.result_label.setProperty("status", "neutral")
            self.refresh_styles(self.result_label)
            self.same_count = 0
            return

        semitone_diff, cent_diff = get_pitch_difference(self.target_freq, freq)
        note_name, _ = freq_to_note_name(freq)

        if self.last_note == note_name and abs(freq - (self.last_freq or 0)) < 1.0:
            self.same_count += 1
        else:
            self.same_count = 0

        self.last_freq = freq
        self.last_note = note_name

        if self.same_count < 2:
            return

        if is_pitch_close(self.target_freq, freq):
            self.result_label.setText(f"✅ Correct! {note_name}")
            self.result_label.setProperty("status", "correct")
            self.set_next_target()
            self.same_count = 0
        else:
            direction = "Sharp" if cent_diff > 0 else "Flat"
            self.result_label.setText(f"❌ Too {direction} by {abs(cent_diff):.1f} cents ({note_name})")
            self.result_label.setProperty("status", "wrong")

        self.refresh_styles(self.result_label)
        self.debug_label.setText(f"Detected: {freq:.2f} Hz | Confidence: {conf:.2f}")

    def refresh_styles(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def setup_styles(self, path):
        self.style_path = path
        self.apply_stylesheet(path)
        # self.watcher = QFileSystemWatcher([path])  # Optional live reload
        # self.watcher.fileChanged.connect(lambda: self.apply_stylesheet(path))

    def apply_stylesheet(self, path):
        try:
            with open(path, 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print("Style reload error:", e)
