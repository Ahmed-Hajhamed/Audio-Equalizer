from pydub import AudioSegment
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

# Define the times (in milliseconds) where you want to start muting
mute_start_times_ms = [ 2055 ,
 7467 ,
 12112,
 14920,
 17072,
 19112,
 24178,
 29216,
 32017,
 34173,
 38670,
 41281,
 42373,
 46231,
 47292,
 48351,
 53038,
 60533,
 61017,
 61048,
 61059,
 69505]  
mute_duration_ms = 500  # Duration of each mute segment in milliseconds


audio_path = 'yes.mp3'  # 
audio_segment = AudioSegment.from_mp3(audio_path)

# Get the duration of the audio in milliseconds
audio_duration_ms = len(audio_segment)
print(f"Audio duration: {audio_duration_ms / 1000} seconds")


muted_audio = audio_segment

for start_time_ms in mute_start_times_ms:
    end_time_ms = start_time_ms + mute_duration_ms

    if end_time_ms > audio_duration_ms:
        end_time_ms = audio_duration_ms

    print(f"Muting from {start_time_ms / 1000} seconds to {end_time_ms / 1000} seconds")
 
    silence = AudioSegment.silent(duration=end_time_ms - start_time_ms)

    muted_audio = muted_audio[:start_time_ms] + silence + muted_audio[end_time_ms:]

output_path = 'yesterday_the_beatles_muted.mp3'
muted_audio.export(output_path, format='mp3')

print(f"Processed audio saved to {output_path}")
