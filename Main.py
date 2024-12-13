import array
import signal
import sys
import copy
import Graph
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog, QSlider, QLabel,QGridLayout
from PyQt5.QtCore import Qt
import GUI
from qt_material import apply_stylesheet
import Mode
import MySignal
import Audiogram
import soundfile as sf
import csv
from SoundPlayer import AudioPlayerWidget
import tempfile

def wiener_filter(signal, noise_detected):
    """
    Apply a Wiener filter to a signal in the frequency domain with a detected noise spectrum.
    
    Parameters:
    - signal (ndarray): The noisy signal in the frequency domain (shape: (N,)).
    - noise_detected (ndarray): The detected noise in the frequency domain (shape: (M,)).
    
    Returns:
    - filtered_signal (ndarray): The filtered signal in the frequency domain (shape: (N,)).
    """
    # Interpolate noise spectrum to match signal length
    noise_interpolated = np.interp(np.linspace(0, 1, len(signal)),
                                   np.linspace(0, 1, len(noise_detected)),
                                   np.abs(noise_detected))
    
    # Compute Power Spectral Densities (PSDs)
    psd_signal = np.abs(signal) ** 2
    psd_noise = noise_interpolated ** 2

    # Compute Wiener filter transfer function
    H = psd_signal / (psd_signal + psd_noise + 1e-10)  # Add small value to avoid division by zero
    
    # Apply the Wiener filter
    filtered_signal = H * signal
    
    return filtered_signal



class MainWindow(QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_mode_name = 'Uniform Mode'
        self.signal_file_path= 'audio/music2.wav'
        self.sliders_layout=None
        self.gain = None
        self.original_signal=None
        self.equalized_signal=None
        self.band_edges= None
        self.frequency_domain=None
        self.number_of_sliders = 10
        self.slider_values = []
        self.fft_of_signal = None
        self.frequencies_of_signal = None
        self.noise_data = None
        self.linear_scale_radioButton.setChecked(True)
        self.spectrogram_checkbox.setChecked(False)
        self.spectrogram_checkbox.stateChanged.connect(self.hide_show_spectrogram)
        self.load_button.clicked.connect(self.load_signal)
        self.save_button.clicked.connect(self.save_signal)

        self.play_pause_button.clicked.connect(lambda: self.original_graph.play_pause(self.play_pause_button))
        self.reset_button.clicked.connect(self.original_graph.rewind_signal)
        self.zoom_in_button.clicked.connect(self.original_graph.zoom_in)
        self.zoom_out_button.clicked.connect(self.original_graph.zoom_out)
        self.speed_up_button.clicked.connect(self.original_graph.speed_up_signal)
        self.speed_down_button.clicked.connect(self.original_graph.speed_down_signal)

        self.confirm_weiner_filter.clicked.connect(self.filter_signal)
        self.reset_signal_after_wiener_filter.clicked.connect(self.reset_signal_of_wiener_filter)

        self.mode_comboBox.currentIndexChanged.connect(self.choose_mode)
        self.linear_scale_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.audiogram_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.load_signal()
        self.switch_audiogram_linear_scale()
        self.hide_show_spectrogram()
        # self.update_audio_palyer()
        # self.original_media_player.set_other_players([self.equlized_media_player])
        # self.equlized_media_player.set_other_players([self.original_media_player])
        self.original_graph.plot_widget.setXLink(self.equalized_graph.plot_widget)
        self.equalized_graph.plot_widget.setYLink(self.original_graph.plot_widget)

    def load_signal(self):
        if self.original_signal is None:
            file_path = self.signal_file_path
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.signal_file_path=file_path
            self.original_signal= MySignal.Signal(mode=self.current_mode_name, file_path=self.signal_file_path)
            self.equalized_signal=copy.deepcopy(self.original_signal)
            self.file_name_label.setText(self.original_signal.signal_name)
            self.fft_of_signal, self.frequencies_of_signal = Mode.compute_fft(self.original_signal.amplitude_data,
                                                                               self.original_signal.sampling_rate)
            # self.frequency_domain_of_orignal_signal = Mode.get_full_frequency_domain(self.fft_of_signal, self.frequencies_of_signal)
            self.band_edges = list(self.original_signal.frquencies_ranges.values())
            self.frequency_domain = Mode.get_full_frequency_domain(self.fft_of_signal, self.frequencies_of_signal)
            
            # Mode.plot_spectrogram(self.original_signal.amplitude_data,
            #                    self.original_signal.sampling_rate, self.original_spectrogram)
            
            self.original_graph.remove_old_curve()
            self.equalized_graph.remove_old_curve()
            self.choose_mode()
            self.original_graph.add_signal(signal= [self.original_signal.time_data,self.original_signal.amplitude_data])

            Mode.plot_spectrogram(self.original_signal.amplitude_data,
                                self.original_signal.sampling_rate, self.original_spectrogram)
                
            self.update_plots()

    def update_plots(self):
        self.set_uniform_frequency_ranges()
        # self.originalGraph.add_signal(signal= [self.original_signal.time_data,self.original_signal.amplitude_data])
        self.equalized_graph.reconstruct_signal_on_equalized_plot(self.equalized_signal.time_data, 
                                                                 self.equalized_signal.amplitude_data)
        Audiogram.plotAudiogram(self.equalized_signal.amplitude_data, 
                                self.equalized_signal.sampling_rate, self.audiogram_plot)
        
        self.frequency_domain = Mode.get_full_frequency_domain(self.fft_of_signal, self.frequencies_of_signal)
        self.frequency_plot.remove_old_curve()
        self.frequency_plot.add_signal(self.frequency_domain, start = False, color = 'r')
        
        if self.spectrogram_checkbox.isChecked():
            Mode.plot_spectrogram(self.equalized_signal.amplitude_data,
                                self.equalized_signal.sampling_rate, self.equalized_spectrogram)
        
        self.update_audio_palyer()
        
    def save_signal(self):
        if self.current_mode_name == 'ECG Abnormalities':
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
            None,  "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options )

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["List1", "List2"])
                for item1, item2 in zip(self.equalized_signal.time_data, self.equalized_signal.amplitude_data):
                    writer.writerow([item1, item2])
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
            None,  "Save Audio File", "", "Audio Wave (*.wav);;All Files (*)", options=options )
            sf.write(file_path, self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate)


    def slider_creator(self, mode_name="Uniform Mode"):
        self.number_of_sliders = 10 if mode_name == "Uniform Mode" else 4
        band_layout = QGridLayout()
        self.gain = [1] * self.number_of_sliders
        self.slider_values.clear()
        for i in range(self.number_of_sliders):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-100)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setFixedHeight(100)
            self.slider_values.append(slider.value())
            slider.valueChanged.connect(lambda value, idx=i: self.apply_gain(value, idx))
            label = QLabel(str(self.names[i]))
            label.setObjectName("slider_1_label")
            label.setFixedHeight(30)
            band_layout.addWidget(label, 1
                                  , i, 1, 1)
            band_layout.addWidget(slider, 0, i, 1, 1)
        return band_layout
    
    def switch_sliders(self):
        while self.slider_layout.count():
            child = self.slider_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        while self.sliders_layout is not None and self.sliders_layout.count():
            child = self.sliders_layout.takeAt(0)
            if child is not None and child.widget() :
                child.widget().deleteLater()
                
    def apply_gain(self, slider_value, slider_index):
        self.slider_values[slider_index] = slider_value
        self.equalized_signal.amplitude_data, self.fft_of_signal = Mode.apply_gain(self.fft_of_signal,
                                                         self.frequencies_of_signal, self.slider_values, self.band_edges)
        self.equalized_signal.time_data = np.linspace(0, len(self.equalized_signal.amplitude_data)/ self.equalized_signal.sampling_rate,
                                                       len(self.equalized_signal.amplitude_data))
        self.update_plots()
        # self.update_audio_palyer()
        
    def choose_mode(self):
        self.current_mode_name = self.mode_comboBox.currentText()
        self.original_signal.mode = self.current_mode_name
        self.equalized_signal.mode = self.current_mode_name
        self.equalized_signal=copy.deepcopy(self.original_signal)
        
        if self.current_mode_name != "Wiener Filter":
            show_layout(self.sliders_layout)
            hide_layout(self.h_layout_of_button_of_wiener)

            self.equalized_signal.frquencies_ranges = MySignal.available_frequencies[self.current_mode_name]
            self.band_edges = list(self.equalized_signal.frquencies_ranges.values())
            self.names = list(self.equalized_signal.frquencies_ranges.keys())
            self.switch_sliders()
            self.graphs_layout.removeItem(self.slider_layout)
            self.graphs_layout.removeItem(self.sliders_layout)
            self.sliders_layout=self.slider_creator(mode_name=self.current_mode_name)
            self.graphs_layout.addLayout(self.sliders_layout, 5, 0, 1, 6)
        else :
            hide_layout(self.sliders_layout)
            show_layout(self.h_layout_of_button_of_wiener)

        Graph.Graph.current_index = 0
        
        if self.current_mode_name == "Wiener Filter" :
            self.frequency_plot.plot_widget.set_selection_mode(True)
        else:
            self.frequency_plot.plot_widget.set_selection_mode(False)
        
        self.update_plots()
        # self.update_audio_palyer()

    def hide_show_spectrogram(self):
        widgets = [self.original_spectrogram, self.equalized_spectrogram,
                    self.original_spectrogram_label, self.equalized_spectrogram_label, self.line_2]
        for widget in widgets:
            if self.spectrogram_checkbox.isChecked():
                # show_layout(widget)
                widget.show()
                widget.setVisible(True)
                self.graphs_layout.removeWidget(self.original_graph.plot_widget)
                self.graphs_layout.removeWidget(self.equalized_graph.plot_widget)
                self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 6)
                self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 6)
            else:
                # hide_layout(widget)
                # self.graphs_layout.removeWidget(widget)
                # widget.hide()
                # widget.setVisible(False)
                self.original_spectrogram.setVisible(False)
                self.equalized_spectrogram.setVisible(False)
                self.original_spectrogram_label.setVisible(False)
                self.equalized_spectrogram_label.setVisible(False)
                self.line_2.setVisible(False)
                self.graphs_layout.removeWidget(self.original_graph.plot_widget)
                self.graphs_layout.removeWidget(self.equalized_graph.plot_widget)
                self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 8)
                self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 8)

        self.update_plots()

    def switch_audiogram_linear_scale(self):
        if self.linear_scale_radioButton.isChecked():
            self.frequency_plot.plot_widget.setVisible(True)
            self.audiogram_plot.setVisible(False)
            self.frequency_plot_label.setText("Linear Scale Frequency")

        elif self.audiogram_radioButton.isChecked():
            self.frequency_plot.plot_widget.setVisible(False)
            self.audiogram_plot.setVisible(True)
            self.frequency_plot_label.setText("Audiogram Scale")

    def update_audio_palyer(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
          sf.write(temp.name, self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate)
        self.original_media_player =AudioPlayerWidget(audio_file=self.signal_file_path)
        self.equlized_media_player =AudioPlayerWidget(audio_file=temp.name)
        self.controls_layout.addWidget(self.original_media_player, 8, 0, 1, 2)
        self.controls_layout.addWidget(self.equlized_media_player, 9, 0, 1, 2)
        self.original_media_player.set_other_players([self.equlized_media_player])
        self.equlized_media_player.set_other_players([self.original_media_player])

    def set_uniform_frequency_ranges(self):
        if self.current_mode_name=='Uniform Mode':
            frequencies= self.frequencies_of_signal
            max_freq=np.max(frequencies)
            start,end=0,max_freq/10
            for i in range (1, 11):
                self.original_signal.frquencies_ranges[i]=[start,end]
                start+=max_freq/10
                end+=max_freq/10 
    
    def filter_signal(self):
        noise = self.frequency_plot.selected_data[1]
        signal = self.frequency_plot.signal[1]
        signal = wiener_filter(signal, noise)
        # self.frequency_domain.signal[1] = signal

        self.frequency_plot.plot_widget.region.setVisible(False)

    def reset_signal_of_wiener_filter(self):
        pass

def hide_layout(layout):
    if layout is None:
        return
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.hide()

def show_layout(layout):
    if layout is None:
        return
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.show()  # Show each widget

    
app = QApplication(sys.argv)
window = MainWindow()
apply_stylesheet(app, theme='dark_cyan.xml')
window.show()
sys.exit(app.exec_())