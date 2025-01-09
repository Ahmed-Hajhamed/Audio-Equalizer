import os
import numpy as np
import librosa
from scipy.signal import spectrogram

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

class Audio:
    def __init__(self, mode, file_path=None):
        self.mode = mode
        self.time_data = None
        self.amplitude_data = None
        self.signal_name = None
        self.fft = None
        self.frequencies = None
        self.modified_fft = None
        self.frequency_domain = None
        self.band_edges = None
        self.frequency_names = None
        self.frquencies_ranges = None

        if file_path is not None:
            self.file_path = file_path
            self.load_signal()

    def load_signal(self):
        """Load signal data from a CSV, MP3 or mav file."""
        self.signal_name = os.path.splitext(os.path.basename(self.file_path))[0]
        signal_data, self.sampling_rate = librosa.load(self.file_path, sr=44100, duration= 30)
        self.time_data = np.linspace(0, len(signal_data)/ self.sampling_rate, len(signal_data))
        self.amplitude_data = signal_data
        self.change_mode(self.mode)
        self.compute_fft()
        self.get_full_frequency_domain()

    def change_mode(self, mode):
        self.mode = mode
        self.frquencies_ranges = available_frequencies[self.mode]
        self.band_edges = list(self.frquencies_ranges.values())
        self.frequency_names = list(self.frquencies_ranges.keys())

    def compute_fft(self):
        self.fft = np.fft.fft(self.amplitude_data)
        self.modified_fft = self.fft.copy()
        self.frequencies = np.fft.fftfreq(len(self.amplitude_data), d=1.0 /self.sampling_rate)

    def get_full_frequency_domain(self):
        positive_freqs = self.frequencies[:len(self.frequencies) // 2]
        magnitude = np.abs(self.modified_fft)
        positive_magnitude = magnitude[:len(magnitude) // 2]

        magnitude_threshold_ratio = 0.01
        max_magnitude = np.max(positive_magnitude)
        magnitude_threshold = magnitude_threshold_ratio * max_magnitude

        significant_indices = np.where(positive_magnitude > magnitude_threshold)
        positive_freqs = positive_freqs[significant_indices]
        positive_magnitude = positive_magnitude[significant_indices]
        self.frequency_domain = positive_freqs, positive_magnitude

    def apply_gain(self, slider_values):
        self.modified_fft = self.fft.copy()
      
        for slider_idx, slider_value in enumerate(slider_values):
            slider_value = 16 ** (slider_value/50)
            low, high = self.band_edges[slider_idx][0], self.band_edges[slider_idx][1]
            band_mask = np.where((self.frequencies >= low) & (self.frequencies < high))
            self.modified_fft[band_mask] *= slider_value
            self.modified_fft[-band_mask[0]] *= slider_value
        self.reconstruct_signal()
    
    def filter_signal(self, noise_detected, alpha):
        alpha = 1 if alpha == 0 else alpha
        psd_signal = np.abs(self.fft) ** 2
        psd_noise = alpha * np.abs(np.fft.fft(noise_detected, n=len(self.amplitude_data))) ** 2
        wiener_ = psd_signal / (psd_signal + psd_noise + 1e-10)  # Add small value to avoid division by zero
        self.modified_fft = wiener_ * self.fft
        self.reconstruct_signal()

    def reconstruct_signal(self):
        self.amplitude_data = np.fft.ifft(self.modified_fft).real
        self.time_data = np.linspace(0, len(self.amplitude_data)/ self.sampling_rate, len(self.amplitude_data))

    def plot_spectrogram(self, canvas):
        sampled_frequencies, segment_times, Sxx = spectrogram(self.amplitude_data, fs= self.sampling_rate,
                                                               nperseg=128, noverlap=64)
        Sxx_db = 10 * np.log10(Sxx + 1e-10) 

        if canvas.no_label:
            canvas.no_label = False
            canvas.vmin, canvas.vmax = np.min(Sxx_db), np.max(Sxx_db)

        canvas.axes.clear()
        cax = canvas.axes.pcolormesh(segment_times, sampled_frequencies, Sxx_db,
                                      shading='gouraud', cmap='plasma', vmin=canvas.vmin, vmax=canvas.vmax)
        canvas.axes.set_xlabel("Time (s)")
        canvas.axes.set_ylabel("Frequency (Hz)")
        canvas.axes.set_title("Spectrogram")

        if not hasattr(canvas, 'colorbar') or canvas.colorbar is None:
            canvas.colorbar = canvas.figure.colorbar(cax, ax=canvas.axes)
            canvas.colorbar.set_label("Power (dB)")

        else:
            canvas.colorbar.update_normal(cax)

        canvas.draw()
