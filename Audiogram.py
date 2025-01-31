import numpy as np
from scipy.fft import rfft, rfftfreq

def fourierTansformWave(audio=[], sampfreq=440010):
    try:
        audio = audio[:,0]
    except:
        audio = audio[:]

    fourier_transform_magnitude = rfft(audio)
    fourier_transform_magnitude =  np.abs(fourier_transform_magnitude)
    fourier_transform_dB = 20 * np.log10(fourier_transform_magnitude + 1e-6)
    
    fourier_transform_freq = rfftfreq(len(audio), 1 / sampfreq)
    fourier_transform_freq = np.real(fourier_transform_freq)

    return fourier_transform_dB , fourier_transform_freq

def get_audiogram_data(fourier_dB, fourier_freq):
    audiogram_frequencies = [0, 50, 100, 200, 400, 800 , 1600 , 2000 , 4000, 8000, 16000, 20000]
    audiogram_dB = []

    for freq in audiogram_frequencies:
        idx = np.argmin(np.abs(fourier_freq - freq))
        audiogram_dB.append(fourier_dB[idx])
    return audiogram_frequencies, audiogram_dB

def custom_transform(x):
        return np.where(x <= 2000, x, 2000 + (x - 2000) * (2000 / 18000))

def plotAudiogram(data, sampling_rate, audiogram_plot):
    fourier_transform_magnitude, fourier_transform_freq = fourierTansformWave(
        audio=data, sampfreq=sampling_rate)
    
    audiogram_frequencies, left_ear = get_audiogram_data(
        fourier_transform_magnitude, fourier_transform_freq)
    
    def custom_transform(x):
        return np.where(x <= 2000, x, 2000 + (x - 2000) * (2000 / 18000))

    transformed_frequencies = custom_transform(np.array(audiogram_frequencies))
    audiogram_plot.axes.clear()
    audiogram_plot.axes.plot(transformed_frequencies, left_ear, 'x-', label="Original Signal", color='black')

    original_ticks = [0, 1000, 2000, 10000, 20000]  
    transformed_ticks = custom_transform(np.array(original_ticks)) 
    audiogram_plot.axes.set_xticks(transformed_ticks)
    audiogram_plot.axes.set_xticklabels([str(tick) for tick in original_ticks])
    audiogram_plot.axes.invert_yaxis()
    # audiogram_plot.axes.set_title("Audiogram")
    audiogram_plot.axes.set_xlabel("Frequency (Hz)")
    audiogram_plot.axes.set_ylabel("Hearing Threshold (dB HL)")
    audiogram_plot.axes.set_yticks(range(-10, 150, 10))  
    audiogram_plot.axes.grid(True)
    audiogram_plot.axes.legend()
    audiogram_plot.draw()