import numpy as np
import sounddevice as sd
from PyQt5.QtWidgets import (
    QPushButton, QSlider, QVBoxLayout, QWidget, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer

class RealTimeMediaPlayer(QWidget):
    def __init__(self, sr=44100, parent=None):
        super().__init__(parent)

        self.sr = sr
        self.audio_buffer = np.array([], dtype=np.float32)
        self.playing = False
        self.stream = None
        self.current_position = 0 
        self.total_samples = 0
        self.other_player = None  

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setFixedWidth(80)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderPressed.connect(self.pause_during_seek)
        self.slider.sliderReleased.connect(self.seek_audio)
        self.slider.setFixedWidth(80)
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setFixedSize(20,50)

        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.slider)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_label)
        layout.addLayout(time_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)

    def set_other_player(self, other_player):
        """Set reference to the other player."""
        self.other_player = other_player

    def toggle_playback(self):
        """Play or pause the audio."""
        if self.playing:
            self.pause_audio()
        else:
            if self.other_player and self.other_player.playing:
                self.other_player.pause_audio()

            self.play_audio()

    def play_audio(self):
        """Start audio playback."""
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.sr,
                channels=1,
                callback=self.audio_callback,
            )
            self.stream.start()

        self.playing = True
        self.play_button.setText("Pause")

    def pause_audio(self):
        """Pause audio playback."""
        self.playing = False
        self.play_button.setText("Play")

    def audio_callback(self, outdata, frames, time, status):
        """Stream audio data in real time."""
        if status:
            print(f"Stream Status: {status}")

        if not self.playing:
            outdata[:] = np.zeros((frames, 1), dtype=np.float32)
            return

        # Get audio data for the current frame
        start = self.current_position
        end = start + frames
        if end > len(self.audio_buffer):
            end = len(self.audio_buffer)

        chunk = self.audio_buffer[start:end]
        if len(chunk) < frames:
            chunk = np.pad(chunk, (0, frames - len(chunk)), mode="constant")

        outdata[:] = chunk.reshape(-1, 1)
        self.current_position = end

    def update_audio_data(self, y):
        """Update the audio buffer with new data."""
        self.audio_buffer = y
        self.total_samples = len(y)
        self.current_position = 0
        self.slider.setRange(0, len(y))
        self.update_ui()

    def pause_during_seek(self):
        """Pause playback during seeking."""
        self.pause_audio()

    def seek_audio(self):
        """Seek to a specific position in the audio."""
        self.current_position = self.slider.value()
        self.play_audio()

    def update_ui(self):
        """Update the slider and time label."""
        if self.audio_buffer is not None and self.total_samples > 0:
            self.slider.setValue(self.current_position)
            current_time = self.current_position // self.sr
            total_time = self.total_samples // self.sr
            self.time_label.setText(
                f"{current_time // 60}:{current_time % 60:02} / {total_time // 60}:{total_time % 60:02}"
            )
