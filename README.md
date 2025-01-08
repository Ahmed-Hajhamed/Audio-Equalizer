# Audio Equalizer App

An advanced **Audio Equalizer Application** designed to enhance your audio processing experience. This app offers versatile equalization modes and powerful visualization tools, enabling users to analyze, modify, and save audio files with ease.

## Features

### 1. **Equalization Modes**
- **Uniform Mode**:
  - Divides the audio signal into 10 uniform frequency ranges.
  - Allows users to adjust the amplitude of each range individually.

- **Animals and Music Mode**:
  - Focuses on three animal voices and two musical instruments.
  - Allows users to equalize specific components in the audio.

- **Vocals and Music Mode**:
  - Targets two alphabetical letters (vocals) and three musical instruments.
  - Enables separate equalization for vocals and instruments in the same audio.

- **Wiener Filter Mode**:
  - Helps filter out noise by analyzing silent periods in the audio.
  - Allows users to select and filter noise effectively.

### 2. **Visualizations**
- **Spectrograms**:
  - Displays the time-frequency representation of the original and equalized audio.

- **Frequency Domain**:
  - Shows the frequency spectrum of the equalized audio.

- **Audiogram**:
  - Provides an intensity versus frequency plot for the equalized audio.

### 3. **Export Results**
- Save the equalized audio as a `.wav` file for further use.

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
   - Modify frequency bands, vocals, or instruments using the intuitive sliders and controls.
4. **Visualize**:
   - View spectrograms, frequency domain plots, and audiograms for better analysis.
5. **Save Results**:
   - Export the processed audio as a `.wav` file.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/audio-equalizer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd audio-equalizer
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Screenshots
(Include screenshots of the app interface and visualizations here)

## Contact
For any queries, feel free to reach out:
- **Email**: yourname@example.com
- **GitHub**: [YourUsername](https://github.com/yourusername)

