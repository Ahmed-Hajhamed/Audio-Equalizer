from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet
import Graph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Define a custom style for gray background
gray_style = {
    'axes.facecolor': '#2E2E2E',    # Dark gray background for axes
    'figure.facecolor': '#2E2E2E',  # Dark gray background for the figure
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
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.no_label = True 
        self.vmin, self.vmax= 0, 0
        super().__init__(fig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1256, 818)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.controls_layout = QtWidgets.QGridLayout()
        self.controls_layout.setObjectName("controls_layout")

        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setObjectName("load_button")
        self.controls_layout.addWidget(self.load_button, 1, 0, 1, 1)

        self.frequency_scale_label = QtWidgets.QLabel(self.centralwidget)
        self.frequency_scale_label.setObjectName("frequency_scale_label")
        self.controls_layout.addWidget(self.frequency_scale_label, 5, 0, 1, 2)

        self.mode_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.mode_comboBox.setObjectName("mode_comboBox")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.setStyleSheet(""" QComboBox { color: 'white';}
                                                    QComboBox QAbstractItemView {color: 'white'; }""")
        self.controls_layout.addWidget(self.mode_comboBox, 3, 0, 1, 2)

        self.choose_mode_label = QtWidgets.QLabel(self.centralwidget)
        self.choose_mode_label.setObjectName("choose_mode_label")
        self.controls_layout.addWidget(self.choose_mode_label, 2, 0, 1, 2)

        self.spectrogram_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.spectrogram_checkbox.setObjectName("spectrogram_checkbox")
        self.controls_layout.addWidget(self.spectrogram_checkbox, 4, 0, 1, 2)

        self.file_name_label = QtWidgets.QLabel(self.centralwidget)
        self.file_name_label.setObjectName("file_name_label")
        self.controls_layout.addWidget(self.file_name_label, 0, 0, 1, 2)

        self.audiogram_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.audiogram_radioButton.setObjectName("audiogram_radioButton")
        self.controls_layout.addWidget(self.audiogram_radioButton, 7, 0, 1, 2)

        # self.controls_layout.addWidget(self.original_media_player, 8, 0, 1, 2)
        # self.controls_layout.addWidget(self.equlized_media_player, 9, 0, 1, 2)

        self.linear_scale_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.linear_scale_radioButton.setObjectName("linear_scale_radioButton")
        self.controls_layout.addWidget(self.linear_scale_radioButton, 6, 0, 1, 2)

        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.controls_layout.addWidget(self.save_button, 1, 1, 1, 1)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.controls_layout.addWidget(self.line, 0, 2, 10, 1)
    
        self.gridLayout_4.addLayout(self.controls_layout, 0, 0, 1, 1)

        self.graphs_layout = QtWidgets.QGridLayout()
        self.graphs_layout.setObjectName("graphs_layout")

        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setObjectName("reset_button")
        self.graphs_layout.addWidget(self.reset_button, 4, 1, 1, 1)

        self.equalized_spectrogram_label = QtWidgets.QLabel(self.centralwidget)
        self.equalized_spectrogram_label.setObjectName("equalized_spectrogram_label")
        self.graphs_layout.addWidget(self.equalized_spectrogram_label, 2, 7, 1, 1)

        self.play_pause_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_pause_button.setObjectName("play_pause_button")
        self.graphs_layout.addWidget(self.play_pause_button, 4, 0, 1, 1)

        self.speed_up_button = QtWidgets.QPushButton(self.centralwidget)
        self.speed_up_button.setObjectName("speed_up_button")
        self.graphs_layout.addWidget(self.speed_up_button, 4, 5, 1, 1)

        self.h_layout_of_button_of_wiener = QtWidgets.QHBoxLayout()
        self.h_layout_of_button_of_wiener.setObjectName("h_layout_of_button_of_wiener")

        self.confirm_weiner_filter = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_weiner_filter.setObjectName("confirm_weiner_filter")
        self.confirm_weiner_filter.setVisible(False)
        self.h_layout_of_button_of_wiener.addWidget(self.confirm_weiner_filter)

        self.reset_signal_after_wiener_filter = QtWidgets.QPushButton(self.centralwidget)
        self.reset_signal_after_wiener_filter.setObjectName("reset_signal_after_wiener_filter")
        self.reset_signal_after_wiener_filter.setVisible(False)
        self.h_layout_of_button_of_wiener.addWidget(self.reset_signal_after_wiener_filter)

        self.graphs_layout.addLayout(self.h_layout_of_button_of_wiener, 5, 0, 1, 6)

        self.equalized_graph = Graph.Graph(self.centralwidget)
        self.equalized_graph.plot_widget.setObjectName("equalized_graph")
        self.graphs_layout.addWidget(self.equalized_graph.plot_widget, 3, 0, 1, 6)

        self.original_graph = Graph.Graph(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.original_graph.plot_widget.sizePolicy().hasHeightForWidth())
        # self.original_graph.plot_widget.setSizePolicy(sizePolicy)
        self.original_graph.plot_widget.setObjectName("original_graph")
        self.graphs_layout.addWidget(self.original_graph.plot_widget, 1, 0, 1, 6)
        self.original_spectrogram_label = QtWidgets.QLabel(self.centralwidget)
        self.original_spectrogram_label.setObjectName("original_spectrogram_label")
        self.graphs_layout.addWidget(self.original_spectrogram_label, 0, 7, 1, 1)

        self.original_spectrogram = SpectrogramPlot(self.centralwidget)
        self.original_spectrogram.setObjectName("original_spectrogram")
        self.graphs_layout.addWidget(self.original_spectrogram, 1, 7, 1, 1)

        self.equalized_spectrogram = SpectrogramPlot(self.centralwidget)
        self.equalized_spectrogram.setObjectName("equalized_spectrogram")
        self.graphs_layout.addWidget(self.equalized_spectrogram, 3, 7, 1, 1)

        self.original_graph_label = QtWidgets.QLabel(self.centralwidget)
        self.original_graph_label.setObjectName("original_graph_label")
        self.graphs_layout.addWidget(self.original_graph_label, 0, 0, 1, 6)

        self.zoom_out_button = QtWidgets.QPushButton(self.centralwidget)
        self.zoom_out_button.setObjectName("zoom_out_button")
        self.graphs_layout.addWidget(self.zoom_out_button, 4, 3, 1, 1)

        self.speed_down_button = QtWidgets.QPushButton(self.centralwidget)
        self.speed_down_button.setObjectName("speed_down_button")
        self.graphs_layout.addWidget(self.speed_down_button, 4, 4, 1, 1)

        self.zoom_in_button = QtWidgets.QPushButton(self.centralwidget)
        self.zoom_in_button.setObjectName("zoom_in_button")
        self.graphs_layout.addWidget(self.zoom_in_button, 4, 2, 1, 1)

        self.equalized_graph_label = QtWidgets.QLabel(self.centralwidget)
        self.equalized_graph_label.setObjectName("equalized_graph_label")
        self.graphs_layout.addWidget(self.equalized_graph_label, 2, 0, 1, 6)

        self.frequency_plot = Graph.Graph(self.centralwidget, is_frequency_domain= True)
        self.frequency_plot.plot_widget.setObjectName("frequency_plot")
        self.frequency_plot.plot_widget.setMaximumWidth(600)
        self.graphs_layout.addWidget(self.frequency_plot.plot_widget, 5, 7, 1, 1)

        self.audiogram_plot = SpectrogramPlot(self.centralwidget)
        self.audiogram_plot.setObjectName("frequency_plot")
        self.graphs_layout.addWidget(self.audiogram_plot, 5, 7, 1, 1)
        self.audiogram_plot.setMaximumWidth(600)
        self.frequency_plot_label = QtWidgets.QLabel(self.centralwidget)
        self.frequency_plot_label.setObjectName("frequency_plot_label")
        self.graphs_layout.addWidget(self.frequency_plot_label, 4, 7, 1, 1)

        self.slider_layout = QtWidgets.QGridLayout()
        self.slider_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.slider_layout.setObjectName("sliders_layout")
        self.graphs_layout.addLayout(self.slider_layout, 5, 0, 1, 6)
        
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.graphs_layout.addWidget(self.line_2, 0, 6, 4, 1)

        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.graphs_layout.addWidget(self.line_3, 5, 6, 1, 1)

        self.gridLayout_4.addLayout(self.graphs_layout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1256, 26))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Audio Equalizer"))
        self.load_button.setText(_translate("MainWindow", "Load"))
        self.frequency_scale_label.setText(_translate("MainWindow", "Frequency Scale:"))
        self.mode_comboBox.setItemText(0, _translate("MainWindow", "Uniform Mode"))
        self.mode_comboBox.setItemText(1, _translate("MainWindow", "Music"))
        self.mode_comboBox.setItemText(2, _translate("MainWindow", "Animal Sounds"))
        self.mode_comboBox.setItemText(3, _translate("MainWindow", "Wiener Filter"))
        self.choose_mode_label.setText(_translate("MainWindow", "Select Mode:"))
        self.spectrogram_checkbox.setText(_translate("MainWindow", "Spectrogram"))
        self.file_name_label.setText(_translate("MainWindow", "File Name"))
        self.audiogram_radioButton.setText(_translate("MainWindow", "Audiogram"))
        self.linear_scale_radioButton.setText(_translate("MainWindow", "Linear Scale"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        self.equalized_spectrogram_label.setText(_translate("MainWindow", "Equalized Spectrogram"))
        self.play_pause_button.setText(_translate("MainWindow", "Play"))
        self.speed_up_button.setText(_translate("MainWindow", "Speed Up"))
        self.original_spectrogram_label.setText(_translate("MainWindow", "Original Audio Spectrogam"))
        self.original_graph_label.setText(_translate("MainWindow", "Original Audio"))
        self.zoom_out_button.setText(_translate("MainWindow", "Zoom Out"))
        self.speed_down_button.setText(_translate("MainWindow", "Speed Down"))
        self.zoom_in_button.setText(_translate("MainWindow", "Zoom In"))
        self.confirm_weiner_filter.setText(_translate("MainWindow", "Confirm"))
        self.reset_signal_after_wiener_filter.setText(_translate("MainWindow", "Reset Signal"))
        self.equalized_graph_label.setText(_translate("MainWindow", "Equalized Audio"))
        self.frequency_plot_label.setText(_translate("MainWindow", "TextLabel"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, "dark_medical.xml")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
