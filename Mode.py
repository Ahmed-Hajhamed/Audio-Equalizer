import numpy as np
from scipy.signal import spectrogram

def compute_fft(signal_amplitudes, sampling_rate):
    fft_result =   np.fft.fft(signal_amplitudes)
    frequencies =   np.fft.fftfreq(len(signal_amplitudes), d=1 /sampling_rate)
    return fft_result, frequencies

def get_full_frequency_domain(fft_of_signal, frequencies_of_signal):
    positive_freqs = frequencies_of_signal[:len(frequencies_of_signal) // 2]
    magnitude = np.abs(fft_of_signal)
    positive_magnitude = magnitude[:len(magnitude) // 2]

    magnitude_threshold_ratio = 0.01
    max_magnitude = np.max(positive_magnitude)
    magnitude_threshold = magnitude_threshold_ratio * max_magnitude

    significant_indices = np.where(positive_magnitude > magnitude_threshold)
    positive_freqs = positive_freqs[significant_indices]
    positive_magnitude = positive_magnitude[significant_indices]
    return positive_freqs, positive_magnitude

def apply_gain(fft_of_signal, frequencies_of_signal, slider_values, band_edges):
    fft_result, frequencies = fft_of_signal, frequencies_of_signal
    modified_fft = fft_result.copy()
    
    for slider_idx, slider_value in enumerate(slider_values):
        slider_value = 16 ** (slider_value/50)
        low, high = band_edges[slider_idx][0], band_edges[slider_idx][1]
        band_mask = np.where((frequencies >= low) & (frequencies < high))
        modified_fft[band_mask] *= slider_value
        modified_fft[-band_mask[0]] *= slider_value
    reconstructed_signal =  np.fft.ifft(modified_fft).real
    return reconstructed_signal, modified_fft

def reconstruct_signal(modified_fft):
    reconstructed_signal = np.fft.ifft(modified_fft).real
    return reconstructed_signal

def plot_spectrogram(signal, sampling_rate, canvas):
    sampled_frequencies, segment_times, Sxx = spectrogram(signal, fs= sampling_rate, nperseg=128, noverlap=64)
    Sxx_db = 10 * np.log10(Sxx + 1e-10) 

    if canvas.no_label:
        canvas.no_label = False
        canvas.vmin, canvas.vmax = np.min(Sxx_db), np.max(Sxx_db)

    canvas.axes.clear()
    cax = canvas.axes.pcolormesh(segment_times, sampled_frequencies, Sxx_db, shading='gouraud', cmap='plasma', vmin=canvas.vmin, vmax=canvas.vmax)
    canvas.axes.set_xlabel("Time (s)")
    canvas.axes.set_ylabel("Frequency (Hz)")
    canvas.axes.set_title("Spectrogram")

    if not hasattr(canvas, 'colorbar') or canvas.colorbar is None:
        canvas.colorbar = canvas.figure.colorbar(cax, ax=canvas.axes)
        canvas.colorbar.set_label("Power (dB)")

    else:
        canvas.colorbar.update_normal(cax)

    canvas.draw()