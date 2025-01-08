import os
import numpy as np
import librosa

available_frequencies = {
    'Uniform Mode': {1:[100, 1000], 2:[100, 1000],
                     3:[100, 1000], 4:[100, 1000],
                    5:[100, 1000],  6:[100, 1000],
                    7:[100, 1000], 8:[100, 1000],
                    9:[100, 1000], 10:[100, 1000] },
    'Vocals and Music': {"Letter A": [40, 400],
              "Letter K": [400, 800],
              "Guitar ": [950, 4000],
              "Violin": [5000, 14000],
              "Piano": [14000, 20000]},
    'Animals and Music': {"Cow": [0, 450],
                      "Chipmunk": [450, 1100],
                      "Whale": [1100, 3000],
                      "Acoordion": [3000, 9000],
                      "Trumpet": [10000, 12000]},
    'Wiener Filter': {"test":0}}

class Signal:
    def __init__(self, mode, file_path=None, x_data=None, y_data=None, name=None):
        self.mode = mode
        if file_path is not None:
            self.file_path = file_path
            self.load_signal()
        else:
            self.time_data = x_data
            self.amplitude_data = y_data
            self.signal_name = name

    def load_signal(self):
        """Load signal data from a CSV, MP3 or mav file."""
        self.signal_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.frquencies_ranges = available_frequencies[self.mode]
        signal_data, self.sampling_rate = librosa.load(self.file_path, sr=44100, duration= 30)
        self.duration = librosa.get_duration(y=signal_data, sr=self.sampling_rate)
        self.time_data = np.linspace(0, len(signal_data)/ self.sampling_rate, len(signal_data))
        self.amplitude_data = signal_data
