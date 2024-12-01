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

def modify_wave (magnitude  , freq , start_index , end_index , new_magnitude  ) : 
    for i in range ( len(magnitude)):
        if  freq[i] >= start_index:
            if freq[i] < end_index:
                freq[i] = new_magnitude
    return magnitude 

def get_audiogram_data(fourier_dB, fourier_freq):
    audiogram_frequencies = [250, 500, 1000, 2000, 4000, 8000] 
    audiogram_dB = []

    for freq in audiogram_frequencies:
        idx = np.argmin(np.abs(fourier_freq - freq))
        audiogram_dB.append(fourier_dB[idx])
    return audiogram_frequencies, audiogram_dB
    
def plotAudiogram(data, sampling_rate, audiogram_plot):
    fourier_transform_magnitude , fourier_transform_freq = fourierTansformWave(audio=data , sampfreq=sampling_rate)
    audiogram_frequencies, left_ear  = get_audiogram_data(fourier_transform_magnitude, fourier_transform_freq)

    refrance = [250, 500, 1000, 2000, 4000, 8000 ]
    left_ref = [20, 20, 20, 35, 70 , 80 ]
    right_ref = [15, 20, 25, 40, 65, 75 ]
    audiogram_plot.axes.clear()

    audiogram_plot.axes.plot(audiogram_frequencies, left_ear, 'x-', label="Original Signal", color='black')
    audiogram_plot.axes.plot(refrance, left_ref, 'o-', label="Left Ear", color='blue')
    audiogram_plot.axes.plot(refrance, right_ref, 's-', label="Right Ear", color='red')

    audiogram_plot.axes.invert_yaxis()
    audiogram_plot.axes.set_title("Audiogram")
    audiogram_plot.axes.set_xlabel("Frequency (Hz)")
    audiogram_plot.axes.set_ylabel("Hearing Threshold (dB HL)")
    audiogram_plot.axes.set_xticks(audiogram_frequencies) 
    audiogram_plot.axes.set_yticks(range(-10, 150, 10))  
    audiogram_plot.axes.grid(True)
    audiogram_plot.axes.legend()
    audiogram_plot.draw()
