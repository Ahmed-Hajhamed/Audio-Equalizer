from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QSlider, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtGui import QIcon


class AudioPlayerWidget(QWidget):
    def __init__(self, speed_up_button, speed_down_button, reset_button): 
        super().__init__()

        self.media_player = QMediaPlayer()
        self.playback_rate = 1.0
        self.media_player.setPlaybackRate(self.playback_rate)

        self.play_button = QPushButton()
        self.play_button.setMaximumWidth(40)
        self.play_button.clicked.connect(self.play_pause_audio)
        set_icon(self.play_button,"icons\play.png" )

        stop_button = QPushButton()
        stop_button.setMaximumWidth(40)
        stop_button.clicked.connect(self.stop_and_reset)
        set_icon(stop_button, "icons\icons8-reset-96.png")

        speed_up_button.clicked.connect(self.increase_speed)
        speed_down_button.clicked.connect(self.decrease_speed)
        reset_button.clicked.connect(self.reset_speed)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderPressed.connect(self.pause_audio_during_seek)
        self.slider.sliderReleased.connect(self.seek_position)
        self.slider.setFixedWidth(200)

        self.time_label = QLabel("0:00")
        self.time_label.setMaximumWidth(50)
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.play_button, 0, 0, 1, 1)
        self.main_layout.addWidget(stop_button, 0, 1, 1, 1)
        self.main_layout.addWidget(self.slider, 1, 0, 1, 2)
        self.main_layout.addWidget(self.time_label, 2, 0, 1, 1)
        # self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(500)

        self.is_seeking = False
        self.is_paused = True

        self.other_players = []

    def update_song(self, file_path):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.time_label.setText("0:00")
        self.slider.setValue(0)
        set_icon(self.play_button, "icons\play.png")
        self.is_paused = True
        self.is_seeking = False

    def set_other_players(self, other_players):
        """Set references to other audio players."""
        self.other_players = other_players

    def stop_and_reset(self):
        self.media_player.stop()
        self.slider.setValue(0)
        self.time_label.setText("0:00")
        self.is_paused = True
        set_icon(self.play_button, "icons\play.png")

    def pause_audio_during_seek(self):
        self.is_seeking = True
        self.media_player.pause()

    def seek_position(self):
        position = self.slider.value()
        self.media_player.setPosition(position)
        self.is_seeking = False
        self.media_player.play()
        self.is_paused = False
        set_icon(self.play_button, "icons\pause.png")

    def update_slider(self, position):
        if not self.is_seeking and self.media_player.duration() > 0:
            self.slider.setValue(position)
        self.update_time_label()

    def update_duration(self, duration):
        self.slider.setRange(0, duration)

    def update_time_label(self):
        position_in_seconds = self.media_player.position() // 1000
        self.time_label.setText(f"{position_in_seconds // 60}:{position_in_seconds % 60:02}")

    def play_pause_audio(self):
        self.remove_icons()
        if self.is_paused:
            for player in self.other_players:
                player.media_player.pause()
                set_icon(player.play_button, "icons\play.png")
            self.media_player.play()
            set_icon(self.play_button, "icons\pause.png")
        else:
            self.media_player.pause()
            set_icon(self.play_button, "icons\play.png")
        self.is_paused = not self.is_paused

    def increase_speed(self):
        self.playback_rate += 0.1
        self.media_player.setPlaybackRate(self.playback_rate)

    def decrease_speed(self):
        self.playback_rate -= 0.1
        self.media_player.setPlaybackRate(max(self.playback_rate, 0.1))

    def reset_speed(self):
        self.media_player.setPlaybackRate(1.0)

    def remove_icons(self):
        self.play_button.setIcon(QIcon())


def set_icon(button, icon_path):
    pixmap = QPixmap(icon_path)
    button.setIcon(QIcon(pixmap))
    button.setIconSize(QSize(30, 30))
    button.setFixedSize(30, 30)
    button.setStyleSheet("border: none; background-color: none;")
