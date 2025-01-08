# Audio Equalizer App

An advanced **Audio Equalizer Application** designed to enhance your audio processing experience. This app offers versatile equalization modes and different visualization tools such as spectrograms, audiograms, and linear frequency scale, enabling users to analyze, modify, and save audio files with ease.

## Features

### 1. **Equalization Modes**
- **Uniform Mode**:
  - Divides the audio signal into 10 uniform frequency ranges.
  - Allows users to adjust the amplitude of each range individually.
![Screenshot 2025-01-08 091156](https://github.com/user-attachments/assets/d7a4a5ee-b330-490b-8521-1224f09e183b)

- **Animals and Music Mode**:
  - Focuses on three animal voices and two musical instruments.
  - Allows users to equalize specific components in the same audio.
![Screenshot 2025-01-08 091309](https://github.com/user-attachments/assets/8865d2e5-5fbd-4a6f-9c52-380c16640ee4)

- **Vocals and Music Mode**:
  - Targets two alphabetical letters (vocals) and three musical instruments.
  - Enables separate equalization for vocals and instruments in the same audio.
![Screenshot 2025-01-08 091457](https://github.com/user-attachments/assets/ff7975f3-de6e-4110-bbfa-7fe1c433937a)

- **Wiener Filter Mode**:
  - Helps filter out noise by analyzing silent periods in the audio.
  - Allows users to select and filter noise using mouse drag.
  - Adjust how much selected noise is filtered out.
![Screenshot 2025-01-08 091754](https://github.com/user-attachments/assets/9e0c637c-1f55-4a98-adc1-352e5ea5629e)

### 2. **Visualizations**
- **Spectrograms**:
  - Displays the time-frequency representation of the original and equalized audio.

- **Frequency Domain**:
  - Shows the frequency spectrum of the equalized audio.

- **Audiogram**:
  - Provides an intensity versus frequency plot for the equalized audio.

### 3. **Export Results**
- Save the equalized audio as a `.wav` file.

## How to Use
1. **Load Audio**:
   - Import an audio file into the application.
2. **Choose a Mode**:
   - Select one of the four equalization modes:
     - Uniform Mode
     - Animals and Music Mode
     - Vocals and Music Mode
     - Wiener Filter Mode
3. **Adjust Parameters**:
   - Modify frequency bands, vocals, or instruments using the sliders.
4. **Visualize**:
   - View spectrograms, frequency domain plots, and audiograms for the analysis of results.
5. **Save Results**:
   - Export the processed audio as a `.wav` file.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmed-Hajhamed/Audio-Equalizer.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Main.py

## Dependencies
- Python 3.x
- `librosa`
- `numpy`
- `matplotlib`
- `PyQt5`
- `scipy`
- `soundfile`

## Contributing
Contributions are welcome! If you have any ideas or improvements, please open an issue or submit a pull request.

## Contact
For any queries, feel free to reach out:
- **GitHub**: [Ahmed-Hajhamed](https://github.com/Ahmed-Hajhamed)

