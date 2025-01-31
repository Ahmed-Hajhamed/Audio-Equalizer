from PyQt5 import QtWidgets
import Graph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import MediaPlayer
from PyQt5.QtCore import Qt

# Custom style for gray background
gray_style = {
    'axes.facecolor': '#2E2E2E',    # Dark gray background for axes
    'figure.facecolor': '#31363b',  # Dark gray background for the figure
    'axes.edgecolor': 'white',      # White edges for axes
    'axes.labelcolor': 'white',     # White labels
    'xtick.color': 'white',         # White tick marks on x-axis
    'ytick.color': 'white',         # White tick marks on y-axis
    'text.color': 'white',          # White text
    'grid.color': '#444444',        # Slightly lighter grid lines
    'grid.linestyle': '--',         # Dashed grid lines
    'lines.color': 'cyan',          # Default line color
    'patch.edgecolor': 'white',     # Edge color for patches
    'legend.facecolor': '#4C4C4C',  # Darker gray background for legends
    'legend.edgecolor': 'white',    # White edges for legends
}
plt.style.use(gray_style)

class SpectrogramPlot(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.no_label = True 
        self.vmin, self.vmax= 0, 0
        super().__init__(fig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.resize(1067, 731)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.sliders_layout = QtWidgets.QGridLayout()
        self.controls_layout = QtWidgets.QVBoxLayout()
        self.spectrograms_layout = QtWidgets.QGridLayout()
        self.frequency_domain_layout = QtWidgets.QGridLayout()
        self.graphs_layout = QtWidgets.QVBoxLayout()
        self.graph_buttons_layout = QtWidgets.QHBoxLayout()
        self.h_layout_of_button_of_wiener = QtWidgets.QHBoxLayout()
        self.graphs_and_spectrograms_layout = QtWidgets.QHBoxLayout()

        self.file_name_label = QtWidgets.QLabel("File Name: ")
        self.file_name_label.setWordWrap(True)
        self.file_name_label.setFixedWidth(200)
        self.load_button = QtWidgets.QPushButton("Load")
        self.load_button.setFixedWidth(200)
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setFixedWidth(200)
        self.choose_mode_label = QtWidgets.QLabel("Choose Mode: ")
        self.choose_mode_label.setFixedWidth(200)
        self.mode_comboBox = QtWidgets.QComboBox()
        self.mode_comboBox.setFixedWidth(200)
        self.spectrogram_checkbox = QtWidgets.QCheckBox("Show Spectrogram")
        self.spectrogram_checkbox.setFixedWidth(200)
        self.frequency_scale_label = QtWidgets.QLabel(" Frequency Scale: ")
        self.frequency_scale_label.setFixedWidth(200)
        self.linear_scale_radioButton = QtWidgets.QRadioButton("Linear Scale")
        self.linear_scale_radioButton.setFixedWidth(200)
        self.audiogram_radioButton = QtWidgets.QRadioButton("Audiogram")
        self.audiogram_radioButton.setFixedWidth(200)

        self.original_graph_label = QtWidgets.QLabel("Original Audio")
        self.original_graph_label.setMaximumHeight(30)
        self.equalized_graph_label = QtWidgets.QLabel("Equalized Audio")
        self.equalized_graph_label.setMaximumHeight(30)
        self.original_spectrogram_label = QtWidgets.QLabel("Original Spectrogram")
        self.original_spectrogram_label.setMaximumHeight(30)
        self.equalized_spectrogram_label = QtWidgets.QLabel("Equalized Spectrogram")
        self.equalized_spectrogram_label.setMaximumHeight(30)
        self.frequency_plot_label = QtWidgets.QLabel("Frequency Domain")
        self.frequency_plot_label.setMaximumHeight(30)

        self.original_graph = Graph.Graph(wiener= True, shading= True)
        self.original_graph.plot_widget.setMinimumWidth(600)
        self.equalized_graph = Graph.Graph(shading= True)
        self.equalized_graph.plot_widget.setMinimumWidth(600)
        self.frequency_plot = Graph.Graph()
        self.original_spectrogram = SpectrogramPlot(width=5, height=3.5)
        self.equalized_spectrogram = SpectrogramPlot(width=5, height=3.5)
        self.audiogram_plot = SpectrogramPlot()
        self.audiogram_plot.setFixedSize(600, 250)
        self.frequency_plot.plot_widget.setFixedSize(500, 250)
        self.original_spectrogram.setFixedSize(600, 250)
        self.equalized_spectrogram.setFixedSize(600, 250)

        self.zoom_in_button = QtWidgets.QPushButton("Zoom In")
        self.zoom_out_button = QtWidgets.QPushButton("Zoom Out")
        self.speed_up_button = QtWidgets.QPushButton("Speed Up")
        self.speed_down_button = QtWidgets.QPushButton("Speed Down")
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.linear_scale_radioButton.setChecked(True)
        self.spectrogram_checkbox.setChecked(False)

        self.original_media_player =MediaPlayer.AudioPlayerWidget(self.speed_up_button, self.speed_down_button, self.reset_button)
        self.equlized_media_player =MediaPlayer.AudioPlayerWidget(self.speed_up_button, self.speed_down_button, self.reset_button)
        self.original_media_player.set_other_players([self.equlized_media_player])
        self.equlized_media_player.set_other_players([self.original_media_player])
        self.original_media_player.media_player.positionChanged.connect(self.original_graph.update_shading_region)
        self.equlized_media_player.media_player.positionChanged.connect(self.equalized_graph.update_shading_region)

        self.line = create_line(horizontal=True)
        self.line_2 = create_line()
        self.line_4 = create_line()
        self.line_3 = create_line(horizontal=True)
        self.line_5 = create_line()
        self.line_6 = create_line(horizontal=True)

        self.file_name_label.setWordWrap(True)
        self.mode_comboBox.addItems(["Uniform Mode", "Vocals and Music", "Animals and Music", "Wiener Filter"])
        self.mode_comboBox.setStyleSheet(""" QComboBox { color: 'white';}
                                QComboBox QAbstractItemView {color: 'white'; }""")
        
        self.confirm_weiner_filter_button = QtWidgets.QPushButton("Confirm")
        self.confirm_weiner_filter_button.setVisible(False)

        self.slider_of_alpha_wiener_filter = QtWidgets.QSlider(Qt.Horizontal)
        self.slider_of_alpha_wiener_filter.setRange(0,1000)
        self.slider_of_alpha_wiener_filter.setVisible(False)

        self.h_layout_of_button_of_wiener.addWidget(self.confirm_weiner_filter_button)
        self.h_layout_of_button_of_wiener.addWidget(self.slider_of_alpha_wiener_filter)

        self.controls_layout.addWidget(self.file_name_label)
        self.controls_layout.addWidget(self.load_button)
        self.controls_layout.addWidget(self.save_button)
        self.controls_layout.addWidget(self.choose_mode_label)
        self.controls_layout.addWidget(self.mode_comboBox)
        self.controls_layout.addWidget(self.spectrogram_checkbox)
        self.controls_layout.addWidget(self.frequency_scale_label)
        self.controls_layout.addWidget(self.linear_scale_radioButton)
        self.controls_layout.addWidget(self.audiogram_radioButton)
        self.controls_layout.addLayout(self.original_media_player.main_layout)
        self.controls_layout.addLayout(self.equlized_media_player.main_layout)
    
        self.graphs_layout.addWidget(self.original_graph_label)
        self.graphs_layout.addWidget(self.original_graph.plot_widget)
        self.graphs_layout.addWidget(self.equalized_graph_label)
        self.graphs_layout.addWidget(self.equalized_graph.plot_widget)

        self.graph_buttons_layout.addWidget(self.zoom_in_button)
        self.graph_buttons_layout.addWidget(self.zoom_out_button)
        self.graph_buttons_layout.addWidget(self.speed_up_button)
        self.graph_buttons_layout.addWidget(self.speed_down_button)
        self.graph_buttons_layout.addWidget(self.reset_button)
        self.graphs_layout.addLayout(self.graph_buttons_layout)
        self.graphs_layout.addWidget(self.line_6)

        self.spectrograms_layout.addWidget(self.original_spectrogram_label, 0, 1, 1, 1)
        self.spectrograms_layout.addWidget(self.original_spectrogram, 1, 1, 1, 1)
        self.spectrograms_layout.addWidget(self.equalized_spectrogram_label, 2, 1, 1, 1)
        self.spectrograms_layout.addWidget(self.equalized_spectrogram, 3, 1, 1, 1)
        self.spectrograms_layout.addWidget(self.line_2, 0, 0, 4, 1)

        self.graphs_and_spectrograms_layout.addLayout(self.graphs_layout)
        self.graphs_and_spectrograms_layout.addLayout(self.spectrograms_layout)

        self.frequency_domain_layout.addWidget(self.frequency_plot_label, 1, 1, 1, 1)
        self.frequency_domain_layout.addWidget(self.frequency_plot.plot_widget, 2, 1, 1, 1)
        self.frequency_domain_layout.addWidget(self.audiogram_plot, 2, 1, 1, 1)
        self.frequency_domain_layout.addWidget(self.line_4, 1, 0, 2, 1)

        self.main_layout.addLayout(self.frequency_domain_layout, 1, 3, 1, 1)
        self.main_layout.addLayout(self.graphs_and_spectrograms_layout, 0, 2, 1, 2)
        self.main_layout.addWidget(self.line, 0, 1, 2, 1)
        self.main_layout.addLayout(self.controls_layout, 0, 0, 2, 1)
        self.main_layout.addLayout(self.sliders_layout, 1, 2, 1, 1)
        self.main_layout.addLayout(self.h_layout_of_button_of_wiener, 1, 2, 1, 1)
        self.main_layout.addWidget(self.line_5, 0, 1, 2, 1)

        self.spectrogram_checkbox.stateChanged.connect(self.hide_show_spectrogram)
        self.load_button.clicked.connect(MainWindow.load_signal)
        self.save_button.clicked.connect(MainWindow.save_signal)
        self.zoom_in_button.clicked.connect(self.original_graph.zoom_in)
        self.zoom_out_button.clicked.connect(self.original_graph.zoom_out)
        self.confirm_weiner_filter_button.clicked.connect(MainWindow.remove_formants)
        self.slider_of_alpha_wiener_filter.sliderReleased.connect(MainWindow.filter_signal)
        self.mode_comboBox.currentIndexChanged.connect(MainWindow.choose_mode)
        self.linear_scale_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        self.audiogram_radioButton.toggled.connect(self.switch_audiogram_linear_scale)
        
        self.original_graph.plot_widget.setXLink(self.equalized_graph.plot_widget)
        self.equalized_graph.plot_widget.setXLink(self.original_graph.plot_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Audio Equalizer")

    def hide_show_spectrogram(self):
        if self.spectrogram_checkbox.isChecked():
            show_layout(self.spectrograms_layout)
        else:
            hide_layout(self.spectrograms_layout)
        self.MainWindow.update_plots()

    def switch_audiogram_linear_scale(self):
        if self.linear_scale_radioButton.isChecked():
            self.frequency_plot.plot_widget.setVisible(True)
            self.audiogram_plot.setVisible(False)
            self.frequency_plot_label.setText("Linear Scale Frequency")

        elif self.audiogram_radioButton.isChecked():
            self.frequency_plot.plot_widget.setVisible(False)
            self.audiogram_plot.setVisible(True)
            self.frequency_plot_label.setText("Audiogram Scale")
        self.MainWindow.update_plots()  
            
    def slider_creator(self, mode_name = "Uniform Mode"):
        self.number_of_sliders = 10 if mode_name == "Uniform Mode" else 5
        band_layout = QtWidgets.QGridLayout()
        self.MainWindow.slider_values.clear()
        for i in range(self.number_of_sliders):
            slider = QtWidgets.QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(2)
            slider.setValue(1)
            slider.setFixedHeight(150)
            self.MainWindow.slider_values.append(slider.value())
            
            label = QtWidgets.QLabel(str(self.MainWindow.equalized_signal.frequency_names[i]))
            label.setMaximumHeight(30)
            if mode_name == "Vocals and Music":
                letter = label.text()
                slider.valueChanged.connect(lambda value, letter = letter : self.MainWindow.remove_formants(value, letter))
            else:
                slider.valueChanged.connect(lambda value, idx=i: self.MainWindow.apply_gain(value, idx))
            band_layout.addWidget(label, 1, i, 1, 1)
            band_layout.addWidget(slider, 0, i, 1, 1)
        band_layout.setSpacing(70)
        return band_layout
    
    def switch_sliders(self):
        while self.sliders_layout is not None and self.sliders_layout.count():
            child = self.sliders_layout.takeAt(0)
            if child is not None and child.widget() :
                child.widget().deleteLater()
                
def create_line(horizontal = False):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine) if horizontal else line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("border: 1px solid cyan;")
        return line

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
            widget.show()
