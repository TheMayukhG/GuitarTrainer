from PyQt6.QtWidgets import QApplication
from gui import GuitarTrainer
import sys

print("App starting...")
app = QApplication(sys.argv)
window = GuitarTrainer()
ret = app.exec()
print(f"App exited with code {ret}")
sys.exit(ret)
