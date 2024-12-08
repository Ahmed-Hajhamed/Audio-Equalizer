from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtGui import QIcon
import Graph
class AudioPlayerWidget(QWidget):
    def __init__(self, audio_file = None, parent=None):
        super().__init__(parent)
        self.is_paused = False
        self.media_player = QMediaPlayer()
        self.audio_file = audio_file
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))

        self.play_button = QPushButton()
        self.play_button.clicked.connect(self.play_audio)
        Graph.set_icon(self.play_button,"icons\play.png" )
        # self.play_button.setFixedWidth(40)
        # pause_button = QPushButton("Pause")
        # pause_button.clicked.connect(self.media_player.pause)

        self.stop_button = QPushButton()
        self.stop_button.clicked.connect(self.stop_and_reset)
        # self.stop_button.setFixedWidth(40)
        Graph.set_icon(self.stop_button, "icons\icons8-reset-96.png" )
        # Create a slider for audio progress
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        # self.slider.setFixedWidth(100)
        self.slider.sliderPressed.connect(self.pause_audio_during_seek)
        self.slider.sliderReleased.connect(self.seek_position)

        self.time_label = QLabel("")

        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        # control_layout.addWidget(pause_button)
        control_layout.addWidget(self.stop_button)

        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.time_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addLayout(slider_layout)

        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(500)

        self.is_seeking = False

        self.other_players = []

    def set_other_players(self, other_players):
        """Set references to other audio players."""
        self.other_players = other_players

    def stop_and_reset(self):
        self.remove_icons()
        self.media_player.stop()
        self.slider.setValue(0)
        self.is_paused = True
        Graph.set_icon(self.play_button, "icons\play.png")
        self.time_label.setText("0:00")

    def pause_audio_during_seek(self):
        self.is_seeking = True
        self.media_player.pause()

    def seek_position(self):
        position = self.slider.value()
        self.media_player.setPosition(position)
        self.is_seeking = False
        self.media_player.play()

    def update_slider(self, position):
        if not self.is_seeking and self.media_player.duration() > 0:
            self.slider.setValue(position)
        self.update_time_label()

    def update_duration(self, duration):
        self.slider.setRange(0, duration)

    def update_time_label(self):
        position_in_seconds = self.media_player.position() // 1000
        self.time_label.setText(f"{position_in_seconds // 60}:{position_in_seconds % 60:02}")

    def play_audio(self):
        self.remove_icons()
        if self.is_paused:
            for player in self.other_players:
                # player.play_audio()
                player.media_player.pause()
                Graph.set_icon(player.play_button, "icons\play.png")
            self.media_player.play()
            Graph.set_icon(self.play_button,"icons\pause.png" )
        else:
            self.media_player.pause()
            Graph.set_icon(self.play_button,"icons\play.png" )
        self.is_paused = not self.is_paused

    def remove_icons(self):
        self.play_button.setIcon(QIcon())