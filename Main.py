import sys
import copy
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import UI
from qt_material import apply_stylesheet
import AudioSignal
import Audiogram
import soundfile as sf


class MainWindow(QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_mode = self.mode_comboBox.currentText()
        self.signal_file_path= "audio\\The Alphabet Song-Finny The Shark.mp3"
        self.original_signal = None
        self.equalized_signal = None
        self.number_of_sliders = 10
        self.slider_values = []
        self.formants_sliders_values ={'e': 1, 'f': 1, 'g': 1, 'xylophone': 1, 'chimes': 1}
        self.noise_data = None
        self.alpha_wiener_filter = 100
        self.load_signal()
        self.switch_audiogram_linear_scale()
        self.hide_show_spectrogram()

    def load_signal(self):
        if self.original_signal is None:
            file_path = self.signal_file_path
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "audio", "Audio Files  *.wav *.mp3 *.m4a")
            
        if file_path:
            self.signal_file_path=file_path
            self.original_signal= AudioSignal.Audio(mode=self.current_mode, file_path=self.signal_file_path)
            self.equalized_signal =  copy.deepcopy(self.original_signal)
            self.file_name_label.setText(self.original_signal.signal_name)

            self.original_graph.add_signal([self.original_signal.time_data, self.original_signal.amplitude_data])
            self.original_signal.plot_spectrogram(self.original_spectrogram)
            self.original_media_player.update_song(self.signal_file_path)
            self.original_media_player.reset_speed()
            self.equlized_media_player.reset_speed()
            self.set_uniform_frequency_ranges()
            self.choose_mode()

    def save_signal(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
                None,  "Save Audio File", "audio", "Audio Wave (*.wav)", options=options)
        if file_path:
            sf.write(file_path, self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate)

    def update_plots(self):
        self.equalized_graph.add_signal([self.equalized_signal.time_data, self.equalized_signal.amplitude_data])
        self.equalized_signal.get_full_frequency_domain()
        self.frequency_plot.add_signal(self.equalized_signal.frequency_domain, color = 'r')
        
        if self.spectrogram_checkbox.isChecked():
            self.equalized_signal.plot_spectrogram(self.equalized_spectrogram)

        if self.audiogram_radioButton.isChecked():
            Audiogram.plotAudiogram(self.equalized_signal.amplitude_data, 
                                    self.equalized_signal.sampling_rate, self.audiogram_plot)
        self.update_audio_palyer()

    def apply_gain(self, slider_value, slider_index):
        self.slider_values[slider_index] = slider_value
        self.equalized_signal.apply_gain(self.slider_values)
        self.update_plots()
        
    def choose_mode(self):
        self.current_mode = self.mode_comboBox.currentText()
        self.original_signal.change_band_edges(self.current_mode)
        self.equalized_signal.change_band_edges(self.current_mode)
        self.equalized_signal=copy.deepcopy(self.original_signal)
        
        if self.current_mode != "Wiener Filter":
            UI.show_layout(self.sliders_layout)
            UI.hide_layout(self.h_layout_of_button_of_wiener)

            self.switch_sliders()
            self.main_layout.removeItem(self.sliders_layout)
            self.sliders_layout=self.slider_creator(mode_name= self.current_mode)
            self.main_layout.addLayout(self.sliders_layout, 1, 2, 1, 1)
            self.original_graph.plot_widget.set_selection_mode(False)
        else :
            UI.hide_layout(self.sliders_layout)
            UI.show_layout(self.h_layout_of_button_of_wiener)
            self.original_graph.plot_widget.set_selection_mode(True)
        self.update_plots()

    def update_audio_palyer(self):
        temp_file = "System Files/temp_file.wav"
        sf.write(temp_file, self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate)
        self.equlized_media_player.update_song(temp_file)

    def set_uniform_frequency_ranges(self):
        if self.current_mode == 'Uniform Mode':
            maximum_frequency = np.max(self.original_signal.frequencies)
            start, end = 0, maximum_frequency/10
            for i in range (1, 11):
                AudioSignal.available_frequencies['Uniform Mode'][i]=[[(start), (end)]]
                start += maximum_frequency/10
                end += maximum_frequency/10 
    
    def filter_signal(self):
        self.alpha_wiener_filter = self.slider_of_alpha_wiener_filter.value()
        if self.original_graph.selected_data is not None:
            if len(self.original_graph.selected_data[1]) > 0 :
                noise = self.original_graph.selected_data[1]
                self.equalized_signal.modified_fft = self.equalized_signal.fft.copy()
                self.equalized_signal.apply_wiener_filter(noise, self.alpha_wiener_filter)
            self.original_graph.plot_widget.region.setVisible(False)
            self.update_plots()

    def remove_formants(self, value, letter):
        self.formants_sliders_values[letter] = value
        self.equalized_signal.modified_fft = self.equalized_signal.fft.copy()
        for formant_name, slider_value in self.formants_sliders_values.items():
            self.equalized_signal.remove_formants(slider_value, formant_name)
        self.update_plots()

app = QApplication(sys.argv)
window = MainWindow()
apply_stylesheet(app, theme='dark_cyan.xml')
window.show()
sys.exit(app.exec_())
