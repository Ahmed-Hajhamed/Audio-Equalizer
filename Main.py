import sys
import copy
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider, QLabel, QGridLayout
from PyQt5.QtCore import Qt
import UI
from qt_material import apply_stylesheet
import AudioSignal
import Audiogram
import soundfile as sf
import tempfile


class MainWindow(QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_mode = 'Uniform Mode'
        self.signal_file_path= 'audio\\A.wav'
        self.sliders_layout = None
        self.original_signal = None
        self.equalized_signal = None
        self.number_of_sliders = 10
        self.slider_values = []
        self.noise_data = None
        self.alpha_wiener_filter = 100
        self.linear_scale_radioButton.setChecked(True)
        self.spectrogram_checkbox.setChecked(False)
        self.spectrogram_checkbox.stateChanged.connect(self.hide_show_spectrogram)
        self.load_button.clicked.connect(self.load_signal)
        self.save_button.clicked.connect(self.save_signal)

        self.zoom_in_button.clicked.connect(self.original_graph.zoom_in)
        self.zoom_out_button.clicked.connect(self.original_graph.zoom_out)
        self.speed_up_button.clicked.connect(self.original_graph.speed_up_signal)
        self.speed_down_button.clicked.connect(self.original_graph.speed_down_signal)

        self.confirm_weiner_filter_button.clicked.connect(self.filter_signal)
        self.slider_of_alpha_wiener_filter.sliderReleased.connect(self.filter_signal)

        self.mode_comboBox.currentIndexChanged.connect(self.choose_mode)
        self.linear_scale_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.audiogram_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.load_signal()
        self.switch_audiogram_linear_scale()
        self.hide_show_spectrogram()

        self.original_graph.plot_widget.setXLink(self.equalized_graph.plot_widget)
        self.equalized_graph.plot_widget.setYLink(self.original_graph.plot_widget)

    def load_signal(self):
        if self.original_signal is None:
            file_path = self.signal_file_path
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "audio", "All Files (*);;Text Files (*.txt)")
            
        if file_path:
            self.signal_file_path=file_path
            self.original_signal= AudioSignal.Audio(mode=self.current_mode, file_path=self.signal_file_path)
            self.equalized_signal =  copy.deepcopy(self.original_signal)
            self.file_name_label.setText(self.original_signal.signal_name)
            
            self.choose_mode()
            self.original_graph.remove_old_curve()
            self.equalized_graph.remove_old_curve()
            self.original_graph.add_signal(self.original_signal.time_data, self.original_signal.amplitude_data)

            self.original_signal.plot_spectrogram(self.original_spectrogram)
            self.original_media_player.update_song(self.signal_file_path)
            self.set_uniform_frequency_ranges()
            self.update_plots()

    def update_plots(self):
        self.equalized_graph.add_signal(self.equalized_signal.time_data, self.equalized_signal.amplitude_data)
        self.equalized_signal.get_full_frequency_domain()
        self.frequency_plot.remove_old_curve()
        self.frequency_plot.add_signal(self.equalized_signal.frequency_domain, color = 'r')
        
        if self.spectrogram_checkbox.isChecked():
            self.equalized_signal.plot_spectrogram(self.equalized_spectrogram)

        if self.audiogram_radioButton.isChecked():
            Audiogram.plotAudiogram(self.equalized_signal.amplitude_data, 
                                    self.equalized_signal.sampling_rate, self.audiogram_plot)
        self.update_audio_palyer()
        
    def save_signal(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
                None,  "Save Audio File", "audio", "Audio Wave (*.wav);;All Files (*)", options=options )
        sf.write(file_path, self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate)

    def slider_creator(self, mode_name = "Uniform Mode"):
        self.number_of_sliders = 10 if mode_name == "Uniform Mode" else 5
        band_layout = QGridLayout()
        self.slider_values.clear()
        for i in range(self.number_of_sliders):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-100)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setFixedHeight(100)
            self.slider_values.append(slider.value())
            slider.valueChanged.connect(lambda value, idx=i: self.apply_gain(value, idx))
            label = QLabel(str(self.equalized_signal.frequency_names[i]))
            label.setFixedHeight(30)
            band_layout.addWidget(label, 1, i, 1, 1)
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
        self.equalized_signal.apply_gain(self.slider_values)
        self.update_plots()
        
    def choose_mode(self):
        self.current_mode = self.mode_comboBox.currentText()
        self.original_signal.change_mode(self.current_mode)
        self.equalized_signal.change_mode(self.current_mode)
        self.equalized_signal=copy.deepcopy(self.original_signal)
        
        if self.current_mode != "Wiener Filter":
            show_layout(self.sliders_layout)
            hide_layout(self.h_layout_of_button_of_wiener)

            self.switch_sliders()
            self.graphs_layout.removeItem(self.slider_layout)
            self.graphs_layout.removeItem(self.sliders_layout)
            self.sliders_layout=self.slider_creator(mode_name= self.current_mode)
            self.graphs_layout.addLayout(self.sliders_layout, 5, 0, 1, 6)
        else :
            hide_layout(self.sliders_layout)
            show_layout(self.h_layout_of_button_of_wiener)

        if self.current_mode == "Wiener Filter" :
            self.original_graph.plot_widget.set_selection_mode(True)
        else:
            self.original_graph.plot_widget.set_selection_mode(False)
        self.update_plots()

    def hide_show_spectrogram(self):
        widgets = [self.original_spectrogram, self.equalized_spectrogram,
                    self.original_spectrogram_label, self.equalized_spectrogram_label, self.line_2]
        for widget in widgets:
            if self.spectrogram_checkbox.isChecked():
                widget.show()
                widget.setVisible(True)
                self.graphs_layout.removeWidget(self.original_graph.plot_widget)
                self.graphs_layout.removeWidget(self.equalized_graph.plot_widget)
                self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 6)
                self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 6)
            else:
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
        self.equlized_media_player.update_song(temp.name)

    def set_uniform_frequency_ranges(self):
        if self.current_mode == 'Uniform Mode':
            max_freq = np.max(self.original_signal.frequencies)
            start, end = 0, max_freq/10
            for i in range (1, 11):
                self.original_signal.frquencies_ranges[i]=[(start), (end)]
                start += max_freq/10
                end += max_freq/10 
    
    def filter_signal(self):
        self.alpha_wiener_filter = self.slider_of_alpha_wiener_filter.value()
        if len(self.original_graph.selected_data[1]) > 0 :
            noise = self.original_graph.selected_data[1]
            self.equalized_signal.filter_signal(noise, self.alpha_wiener_filter)
        self.original_graph.plot_widget.region.setVisible(False)
        self.update_plots()


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
