from PyQt5 import QtCore, QtWidgets
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

# Apply the custom style
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
        MainWindow.resize(1256, 818)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.graphs_layout = QtWidgets.QGridLayout()
        self.controls_layout = QtWidgets.QGridLayout()
        self.slider_layout = QtWidgets.QGridLayout()
        self.slider_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.h_layout_of_button_of_wiener = QtWidgets.QHBoxLayout()
        self.sliders_layout = QtWidgets.QGridLayout()

        self.load_button = QtWidgets.QPushButton("Load")
        self.frequency_scale_label = QtWidgets.QLabel("Frequency Scale:")
        self.choose_mode_label = QtWidgets.QLabel("Select Mode:")
        self.spectrogram_checkbox = QtWidgets.QCheckBox("Spectrogram")
        self.file_name_label = QtWidgets.QLabel("File Name")
        self.file_name_label.setWordWrap(True)
        self.audiogram_radioButton = QtWidgets.QRadioButton("Audiogram")
        self.linear_scale_radioButton = QtWidgets.QRadioButton("Linear Scale")
        self.save_button = QtWidgets.QPushButton("Save")
        self.line = create_line()
        self.linear_scale_radioButton.setChecked(True)
        self.spectrogram_checkbox.setChecked(False)
        
        self.controls_layout.addWidget(self.load_button, 1, 0, 1, 1)
        self.controls_layout.addWidget(self.frequency_scale_label, 5, 0, 1, 2)

        self.mode_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.mode_comboBox.addItems(["Uniform Mode", "Vocals and Music", "Animals and Music", "Wiener Filter"])
        self.mode_comboBox.setStyleSheet(""" QComboBox { color: 'white';}
                                                    QComboBox QAbstractItemView {color: 'white'; }""")
        
        self.original_spectrogram = SpectrogramPlot()
        self.equalized_spectrogram = SpectrogramPlot()

        self.original_graph = Graph.Graph(wiener=True, shading=True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        self.equalized_graph = Graph.Graph(shading=True)

        self.audiogram_plot = SpectrogramPlot(width= 3, height=2)

        self.frequency_plot = Graph.Graph()
        self.frequency_plot.plot_widget.setMaximumWidth(600)
        self.frequency_plot_label = QtWidgets.QLabel("Frequency Plot")
        
        self.original_graph_label = QtWidgets.QLabel("Original Audio")
        self.speed_down_button = QtWidgets.QPushButton("Speed Down")
        self.equalized_graph_label = QtWidgets.QLabel("Equalized Audio")
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.zoom_in_button = QtWidgets.QPushButton("Zoom In")
        self.zoom_out_button = QtWidgets.QPushButton("Zoom Out")
        self.equalized_spectrogram_label = QtWidgets.QLabel("Equalized Spectrogram")
        self.speed_up_button = QtWidgets.QPushButton("Speed Up")
        self.original_spectrogram_label = QtWidgets.QLabel("Original Audio Spectrogam")
        self.line_2 = create_line()
        self.line_3 = create_line()

        self.original_media_player =MediaPlayer.AudioPlayerWidget(self.speed_up_button, self.speed_down_button, self.reset_button)
        self.equlized_media_player =MediaPlayer.AudioPlayerWidget(self.speed_up_button, self.speed_down_button, self.reset_button)
        self.original_media_player.set_other_players([self.equlized_media_player])
        self.equlized_media_player.set_other_players([self.original_media_player])

        self.controls_layout.addWidget(self.mode_comboBox, 3, 0, 1, 2)
        self.controls_layout.addWidget(self.choose_mode_label, 2, 0, 1, 2)
        self.controls_layout.addWidget(self.spectrogram_checkbox, 4, 0, 1, 2)     
        self.controls_layout.addWidget(self.file_name_label, 0, 0, 1, 2)       
        self.controls_layout.addWidget(self.audiogram_radioButton, 7, 0, 1, 2)   
        self.controls_layout.addWidget(self.linear_scale_radioButton, 6, 0, 1, 2)
        self.controls_layout.addWidget(self.save_button, 1, 1, 1, 1)
        self.controls_layout.addWidget(self.line, 0, 2, 10, 1)
        self.controls_layout.addWidget(self.original_media_player, 8, 0, 1, 2)
        self.controls_layout.addWidget(self.equlized_media_player, 9, 0, 1, 2)

        self.confirm_weiner_filter_button = QtWidgets.QPushButton("Confirm")
        self.confirm_weiner_filter_button.setVisible(False)

        self.slider_of_alpha_wiener_filter = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_of_alpha_wiener_filter.setRange(0,1000)
        self.slider_of_alpha_wiener_filter.setVisible(False)

        self.h_layout_of_button_of_wiener.addWidget(self.confirm_weiner_filter_button)
        self.h_layout_of_button_of_wiener.addWidget(self.slider_of_alpha_wiener_filter)

        self.graphs_layout.addWidget(self.equalized_spectrogram_label, 2, 7, 1, 1)
        self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 6)
        self.graphs_layout.addWidget(self.original_spectrogram_label, 0, 7, 1, 1)
        self.graphs_layout.addWidget(self.original_spectrogram, 1, 7, 1, 1)
        self.graphs_layout.addWidget(self.equalized_spectrogram, 3, 7, 1, 1)
        self.graphs_layout.addWidget(self.original_graph_label, 0, 0, 1, 6)
        self.graphs_layout.addWidget(self.zoom_out_button, 4, 1, 1, 1)
        self.graphs_layout.addWidget(self.speed_down_button, 4, 2, 1, 1)
        self.graphs_layout.addWidget(self.zoom_in_button, 4, 0, 1, 1)
        self.graphs_layout.addWidget(self.speed_up_button, 4, 3, 1, 1)
        self.graphs_layout.addWidget(self.reset_button, 4, 4, 1, 1) 
        self.graphs_layout.addWidget(self.equalized_graph_label, 2, 0, 1, 6)
        self.graphs_layout.addWidget(self.frequency_plot.plot_widget, 5, 7, 1, 1)
        self.graphs_layout.addWidget(self.audiogram_plot, 5, 7, 1, 1)
        self.graphs_layout.addWidget(self.frequency_plot_label, 4, 7, 1, 1)
        self.graphs_layout.addLayout(self.slider_layout, 5, 0, 1, 6)
        self.graphs_layout.addWidget(self.line_2, 0, 6, 4, 1)
        self.graphs_layout.addWidget(self.line_3, 5, 6, 1, 1)
        self.graphs_layout.addLayout(self.h_layout_of_button_of_wiener, 5, 0, 1, 6)
        self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 6)

        self.original_media_player.media_player.positionChanged.connect(self.original_graph.update_shading_region)
        self.equlized_media_player.media_player.positionChanged.connect(self.equalized_graph.update_shading_region)

        self.main_layout.addLayout(self.controls_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.graphs_layout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Audio Equalizer")

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
                widget.hide()
                widget.setVisible(False)
                self.graphs_layout.removeWidget(self.original_graph.plot_widget)
                self.graphs_layout.removeWidget(self.equalized_graph.plot_widget)
                self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 8)
                self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 8)
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
            
    def slider_creator(self, mode_name = "Uniform Mode"):
        self.number_of_sliders = 10 if mode_name == "Uniform Mode" else 5
        band_layout = QtWidgets.QGridLayout()
        self.slider_values.clear()
        for i in range(self.number_of_sliders):
            slider = QtWidgets.QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(2)
            slider.setValue(1)
            slider.setFixedHeight(100)
            self.MainWindow.slider_values.append(slider.value())
            slider.valueChanged.connect(lambda value, idx=i: self.MainWindow.apply_gain(value, idx))
            label = QtWidgets.QLabel(str(self.MainWindow.equalized_signal.frequency_names[i]))
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
                
def create_line():
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
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
            widget.show()  # Show each widget
    