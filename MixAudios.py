import numpy as np
import soundfile as sf
import librosa
# use this code to mix two audio files ex. animals and music

# Load the two audio files
path_1 = "audio\\animals_new.wav" # path to the original audio file
path_2 = "audio\\musical instruments.wav" # path to the audio file to be mixed
output_path = "mixed_audio.wav"
sampling_rate_1:int = 22050
sampling_rate_2:int = 22050

offset = 114  # seconds
duration = 14  # seconds
audio1, sampling_rate_1 = librosa.load(path_1, sr=sampling_rate_1)
audio2, sampling_rate_2 = librosa.load(path_2, sr=sampling_rate_2, offset= offset, duration=duration)

audio1_duration = librosa.get_duration(y=audio1, sr=sampling_rate_1)

# print(audio1_duration * sampling_rate_1, len(audio2))
audio2 = np.pad(audio2, (0, int(audio1_duration * sampling_rate_1 - len(audio2))), "symmetric")

# Ensure the same sampling rate

# Match lengths by truncation or zero-padding
# min_len = min(len(audio1), len(audio2))
# audio1 = audio1[:min_len]
# audio2 = audio2[:min_len]

# Add the audio signals
mixed_audio = audio1 + audio2

# Normalize to prevent clipping
mixed_audio = mixed_audio / np.max(np.abs(mixed_audio))

# Save the mixed audio
sf.write(output_path, mixed_audio, sampling_rate_2)
