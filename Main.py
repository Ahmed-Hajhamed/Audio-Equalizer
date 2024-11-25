import sys
import copy
import Graph
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog, QSlider, QLabel,QGridLayout
from PyQt5.QtCore import Qt
import UI 
from qt_material import apply_stylesheet
import Mode
import MySignal
import Audiogram
import soundfile as sf
import csv

class MainWindow(QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_mode_name = 'Uniform Mode'
        self.signal_file_path= 'audio\\file_example_WAV_1MG.wav'
        self.sliders_layout=None
        self.gain = None
        self.original_signal=None
        self.equalized_signal=None
        self.band_edges= None
        self.frequency_domain=None
        self.number_of_sliders = 10
        self.slider_values = []
        
        self.linearScaleRadioButton.setChecked(True)
        self.spectrugramCheckBox.setChecked(True)
        self.spectrugramCheckBox.stateChanged.connect(self.hide_show_spectrogram)
        self.loadButton.clicked.connect(self.load_signal)
        self.saveButton.clicked.connect(self.save_signal)

        self.playButton.clicked.connect(lambda: self.originalGraph.play_pause(self.playButton))
        self.resetButton.clicked.connect(self.originalGraph.rewind_signal)
        self.zoomInButton.clicked.connect(self.originalGraph.zoom_in)
        self.zoomOutButton.clicked.connect(self.originalGraph.zoom_out)
        self.speedUpButton.clicked.connect(self.originalGraph.speed_up_signal)
        self.speedDownButton.clicked.connect(self.originalGraph.speed_down_signal)

        self.modeComboBox.currentIndexChanged.connect(self.choose_mode)
        self.linearScaleRadioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.audiogramRadioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.load_signal()

    def load_signal(self):
        if self.original_signal is None:
            file_path = self.signal_file_path
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.signal_file_path=file_path
            self.original_signal= MySignal.Signal(mode=self.current_mode_name, file_path=self.signal_file_path)
            self.equalized_signal=copy.deepcopy(self.original_signal)

            self.band_edges = list(self.original_signal.frquencies_ranges.values())
            self.originalGraph.add_signal(signal= [self.original_signal.time_data,self.original_signal.amplitude_data])
            self.equalizedGraph.add_signal([self.equalized_signal.time_data, self.equalized_signal.amplitude_data])

            Audiogram.plotAudiogram(self.equalized_signal.amplitude_data, self.equalized_signal.sampling_rate, 
                                                                                    self.audiogramPlot)
            self.frequency_domain = Mode.get_full_frequency_domain(self.equalized_signal.amplitude_data, 
                                                                   self.equalized_signal.sampling_rate)
            self.frequencyDomainPlot.remove_old_curve()
            self.frequencyDomainPlot.add_signal(self.frequency_domain, start = False, color = 'r')
            Mode.plot_spectrogram(self.original_signal.amplitude_data,
                                   self.original_signal.sampling_rate, self.originalSpectrugram)
            Mode.plot_spectrogram(self.equalized_signal.amplitude_data,
                                  self.equalized_signal.sampling_rate, self.equalizedSpecrtugram)
            self.switch_audiogram_linear_scale()
            
            self.choose_mode()
            if self.current_mode_name=='Uniform Mode':
                frequencies= Mode.compute_fft(self.original_signal.amplitude_data, self.original_signal.sampling_rate)[1]
                max_freq=np.max(frequencies)
                start,end=0,max_freq/10
                for i in range (1, 11):
                    self.original_signal.frquencies_ranges[i]=[start,end]
                    start+=max_freq/10
                    end+=max_freq/10
            self.update_plots()

    def update_plots(self):
        self.originalGraph.add_signal(signal= [self.original_signal.time_data,self.original_signal.amplitude_data])
        self.equalizedGraph.reconstruct_signal_on_equalized_plot(self.equalized_signal.time_data, 
                                                                 self.equalized_signal.amplitude_data)
        Audiogram.plotAudiogram(self.equalized_signal.amplitude_data, 
                                self.equalized_signal.sampling_rate, self.audiogramPlot)
        self.frequency_domain = Mode.get_full_frequency_domain(self.equalized_signal.amplitude_data, 
                                                               self.equalized_signal.sampling_rate)
        self.frequencyDomainPlot.remove_old_curve()
        self.frequencyDomainPlot.add_signal(self.frequency_domain, start = False, color = 'r')

        Mode.plot_spectrogram(self.original_signal.amplitude_data,
                               self.original_signal.sampling_rate, self.originalSpectrugram)
        Mode.plot_spectrogram(self.equalized_signal.amplitude_data,
                               self.equalized_signal.sampling_rate, self.equalizedSpecrtugram)

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
            band_layout.addWidget(label, 3, i, 1, 1)
            band_layout.addWidget(slider, 2, i, 1, 1)
        return band_layout
    
    def switch_sliders(self):
        while self.gridLayout_7.count():
            child = self.gridLayout_7.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        while self.sliders_layout is not None and self.sliders_layout.count():
            child = self.sliders_layout.takeAt(0)
            if child is not None and child.widget() :
                child.widget().deleteLater()
                
    def apply_gain(self, slider_value, slider_index):
        self.slider_values[slider_index] = slider_value
        self.equalized_signal.amplitude_data = Mode.apply_gain(self.original_signal.amplitude_data, self.slider_values,
                                                               self.band_edges, self.original_signal.sampling_rate)
        self.update_plots()
        
    def choose_mode(self):
        self.current_mode_name = self.modeComboBox.currentText()
        self.original_signal.mode = self.current_mode_name
        self.equalized_signal.mode = self.current_mode_name
        self.equalized_signal.frquencies_ranges = MySignal.available_frequencies[self.current_mode_name]
        self.band_edges = list(self.equalized_signal.frquencies_ranges.values())
        self.names = list(self.equalized_signal.frquencies_ranges.keys())
        self.switch_sliders()
        self.gridLayout_12.removeItem(self.gridLayout_7)
        self.gridLayout_12.removeItem(self.sliders_layout)
        self.sliders_layout=self.slider_creator(mode_name=self.current_mode_name)
        self.gridLayout_12.addLayout(self.sliders_layout,7,2,1,2)
        Graph.Graph.current_index = 0
        self.original_signal= MySignal.Signal(mode=self.current_mode_name, file_path=self.signal_file_path)
        self.equalized_signal=copy.deepcopy(self.original_signal)
        self.update_plots()

    def hide_show_spectrogram(self):
        layouts = [self.gridLayout, self.gridLayout_2, self.gridLayout_20, self.gridLayout_14]
        for layout in layouts:
            if self.spectrugramCheckBox.isChecked():
                show_layout(layout)
            else:
                hide_layout(layout)

    def switch_audiogram_linear_scale(self):
        if self.linearScaleRadioButton.isChecked():
            self.frequencyDomainPlot.plot_widget.setVisible(True)
            self.audiogramPlot.setVisible(False)
        elif self.audiogramRadioButton.isChecked():
            self.frequencyDomainPlot.plot_widget.setVisible(False)
            self.audiogramPlot.setVisible(True)

def hide_layout(layout):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.hide()

def show_layout(layout):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.show()  # Show each widget



app = QApplication(sys.argv)
window = MainWindow()
apply_stylesheet(app, theme='dark_teal.xml')
window.show()
sys.exit(app.exec_())