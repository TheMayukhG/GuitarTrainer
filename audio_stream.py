import numpy as np
import sounddevice as sd
import librosa
import traceback
import threading
import queue

SAMPLE_RATE = 22050
FRAME_SIZE = 2048
HOP_SIZE = 512
CONFIDENCE_THRESHOLD = 0.85


class AudioPitchStream:
    def __init__(self, callback):
        self.callback = callback  # Will be a signal.emit(...)
        self.buffer = np.zeros(FRAME_SIZE, dtype=np.float32)
        self.running = False
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.process_queue, daemon=True)

    def _audio_callback(self, indata, frames, time_info, status):
        try:
            if status:
                print(f"zsStream status: {status}")
            mono = np.mean(indata, axis=1).astype(np.float32)
            self.buffer = np.concatenate([self.buffer[len(mono):], mono])
            self.q.put(self.buffer.copy())
        except Exception as e:
            print("Callback error:", e)
            traceback.print_exc()

    def process_queue(self):
        while True:
            try:
                buffer = self.q.get()
                pitch = librosa.yin(
                    buffer,
                    fmin=80,
                    fmax=1000,
                    sr=SAMPLE_RATE,
                    frame_length=FRAME_SIZE,
                    hop_length=HOP_SIZE,
                )[0]
                confidence = 1.0 if pitch > 0 else 0.0
                if confidence >= CONFIDENCE_THRESHOLD:
                    self.callback(pitch, confidence)
                else:
                    self.callback(0.0, confidence)
            except Exception as e:
                print("Worker error:", e)
                traceback.print_exc()

    def start(self):
        if self.running:
            return
        try:
            self.stream = sd.InputStream(
                channels=1,
                samplerate=SAMPLE_RATE,
                callback=self._audio_callback,
                blocksize=0,
                dtype='float32',
                latency='high',
            )
            self.stream.start()
            self.thread.start()
            self.running = True
            print("Audio stream started.")
        except Exception as e:
            print("Failed to start stream:")
            traceback.print_exc()

    def stop(self):
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                print("Audio stream stopped.")
            except Exception as e:
                print("Error stopping stream:")
                traceback.print_exc()
        self.running = False
