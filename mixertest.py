import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer

class AudioPlayerWidget(QWidget):
    def __init__(self, audio_file = None, parent=None):
        super().__init__(parent)

        # Create a media player object
        self.media_player = QMediaPlayer()
        self.audio_file = audio_file
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))

        # Create UI elements
        play_button = QPushButton("Play")
        play_button.clicked.connect(self.play_audio)

        pause_button = QPushButton("Pause")
        pause_button.clicked.connect(self.media_player.pause)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_and_reset)

        # Create a slider for audio progress
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderPressed.connect(self.pause_audio_during_seek)
        self.slider.sliderReleased.connect(self.seek_position)

        # Label to show the current time
        self.time_label = QLabel("0:00")

        # Connect signals for updating UI
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration)

        # Layout setup
        control_layout = QHBoxLayout()
        control_layout.addWidget(play_button)
        control_layout.addWidget(pause_button)
        control_layout.addWidget(stop_button)

        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.time_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addLayout(slider_layout)

        self.setLayout(main_layout)

        # Timer for updating the time label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(500)

        self.is_seeking = False

        # This will hold the reference to other players
        self.other_players = []

    def set_other_players(self, other_players):
        """Set references to other audio players."""
        self.other_players = other_players

    def stop_and_reset(self):
        self.media_player.stop()
        self.slider.setValue(0)
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
        """Start playing the audio, stop other players if necessary."""
        # Stop all other players before starting this one
        for player in self.other_players:
            # player.stop_and_reset()
            player.media_player.pause()

        # Now play this audio
        self.media_player.play()


# # Main window class to add the AudioPlayerWidget
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Main Window with Audio Player")
#         self.setGeometry(100, 100, 500, 300)

#         # Create two instances of the audio player widget
#         audio_player_1 = AudioPlayerWidget(audio_file="C:\\Users\\VICTUS\\Downloads\\file_example_WAV_1MG.wav")  # Replace with actual file
#         audio_player_2 = AudioPlayerWidget(audio_file="C:\\Users\\VICTUS\\Downloads\\Passenger _ Let Her Go (Official Video) - Passenger (youtube).mp3")  # Replace with actual file

#         # Set the other players for each player
#         audio_player_1.set_other_players([audio_player_2])
#         audio_player_2.set_other_players([audio_player_1])

#         # Set up the layout to hold both audio players
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(audio_player_1)
#         main_layout.addWidget(audio_player_2)

#         # Create a central widget to hold the layout
#         central_widget = QWidget()
#         central_widget.setLayout(main_layout)

#         # Set the central widget of the window
#         self.setCentralWidget(central_widget)


# # Run the application
# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# sys.exit(app.exec_())
