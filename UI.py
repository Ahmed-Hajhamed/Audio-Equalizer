from PyQt5 import QtCore, QtWidgets
from Graph import Graph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from MediaPlayer import RealTimeMediaPlayer
from mixertest import AudioPlayerWidget
class spectrogramPlot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.no_label = True 
        self.vmin, self.vmax= 0, 0
        super().__init__(fig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1916, 961)
        MainWindow.setStyleSheet("")
        # self.original_media_player = RealTimeMediaPlayer()
        # self.equlized_media_player = RealTimeMediaPlayer()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_12 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout_au = QtWidgets.QGridLayout()
        self.gridLayout_au.setObjectName("gridLayout_2")

        self.gridLayout_in = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_in.setObjectName("gridLayout_2")

        self.equalizedSpecrtugram = spectrogramPlot(self.centralwidget)
        self.equalizedSpecrtugram.setMaximumSize(QtCore.QSize(400, 400))
        self.equalizedSpecrtugram.setObjectName("equalizedSpecrtugram")

        self.gridLayout_2.addWidget(self.equalizedSpecrtugram, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_2, 5, 3, 2, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")

        self.originalFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.originalFileLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.originalFileLabel.setObjectName("originalFileLabel")

        self.gridLayout_15.addWidget(self.originalFileLabel, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_15, 0, 2, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.originalGraph = Graph(self.centralwidget)
        # self.originalGraph.plot_widget.setMaximumSize(QtCore.QSize(600, 400))
        self.originalGraph.plot_widget.setObjectName("originalGraph")

        self.gridLayout_6.addWidget(self.originalGraph.plot_widget, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_4, 1, 2, 2, 1)
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")

        self.equalizedSpectrugramLabel = QtWidgets.QLabel(self.centralwidget)
        self.equalizedSpectrugramLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.equalizedSpectrugramLabel.setObjectName("equalizedSpectrugramLabel")

        self.gridLayout_20.addWidget(self.equalizedSpectrugramLabel, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_20, 4, 3, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.modeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.modeComboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.modeComboBox.setObjectName("modeComboBox")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.setStyleSheet(""" QComboBox { color: 'white';}
                                                    QComboBox QAbstractItemView {color: 'white'; }""")

        self.gridLayout_10.addWidget(self.modeComboBox, 2, 0, 1, 1)
        self.selectModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectModeLabel.setMaximumSize(QtCore.QSize(200, 50))
        self.selectModeLabel.setObjectName("selectModeLabel")

        self.gridLayout_10.addWidget(self.selectModeLabel, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_10, 2, 0, 1, 1)
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")

        self.spectrugramCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.spectrugramCheckBox.setObjectName("spectrugramCheckBox")

        self.gridLayout_17.addWidget(self.spectrugramCheckBox, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_17, 4, 0, 1, 1)

        self.gridLayout_player = QtWidgets.QGridLayout()
        self.gridLayout_player.setObjectName("gridLayout_player")

        self.gridLayout_player.setGeometry
        self.gridLayout_12.addLayout(self.gridLayout_player, 6,0,1,1)

        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")

        self.equalizedFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.equalizedFileLabel.setMaximumSize(QtCore.QSize(1000, 50))
        self.equalizedFileLabel.setObjectName("equalizedFileLabel")

        self.gridLayout_16.addWidget(self.equalizedFileLabel, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_16, 4, 2, 1, 1)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.gridLayout_12.addWidget(self.line_2, 0, 4, 8, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.equalizedGraph = Graph(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.equalizedGraph.plot_widget.sizePolicy().hasHeightForWidth())

        self.equalizedGraph.plot_widget.setSizePolicy(sizePolicy)
        # self.equalizedGraph.plot_widget.setMaximumSize(QtCore.QSize(600, 300))
        self.equalizedGraph.plot_widget.setObjectName("equalizedGraph")

        self.gridLayout_5.addWidget(self.equalizedGraph.plot_widget, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_5, 5, 2, 2, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setMaximumSize(QtCore.QSize(100, 50))
        self.saveButton.setObjectName("saveButton")

        self.gridLayout_3.addWidget(self.saveButton, 1, 0, 1, 1)
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setMaximumSize(QtCore.QSize(100, 50))
        self.loadButton.setObjectName("loadButton")

        self.gridLayout_3.addWidget(self.loadButton, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_3, 0, 0, 2, 1)
        self.gridLayout_21 = QtWidgets.QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.gridLayout_21.addWidget(self.line, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_21, 0, 1, 8, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.speedUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.speedUpButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.speedUpButton.setObjectName("speedUpButton")

        self.gridLayout_8.addWidget(self.speedUpButton, 1, 5, 1, 1)
        self.speedDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.speedDownButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.speedDownButton.setObjectName("speedDownButton")

        self.gridLayout_8.addWidget(self.speedDownButton, 1, 6, 1, 1)
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.resetButton.setObjectName("resetButton")

        self.gridLayout_8.addWidget(self.resetButton, 1, 2, 1, 1)
        self.zoomInButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomInButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.zoomInButton.setObjectName("zoonInButton")

        self.gridLayout_8.addWidget(self.zoomInButton, 1, 3, 1, 1)
        self.zoomOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomOutButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.zoomOutButton.setObjectName("zoomOutButton")

        self.gridLayout_8.addWidget(self.zoomOutButton, 1, 4, 1, 1)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.playButton.setObjectName("playButton")

        self.gridLayout_8.addWidget(self.playButton, 1, 1, 1, 1)
        self.linearScaleRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.linearScaleRadioButton.setMaximumSize(QtCore.QSize(120, 20))
        self.linearScaleRadioButton.setObjectName("radioButton_2")

        self.frequency_label = QtWidgets.QLabel(self.centralwidget)
        self.frequency_label.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frequency_label.setObjectName("slider_1_label")

        self.gridLayout_au.addWidget(self.linearScaleRadioButton, 9, 9, 8, 7)
        self.audiogramRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.audiogramRadioButton.setMaximumSize(QtCore.QSize(120, 20))
        self.audiogramRadioButton.setObjectName("radioButton")

        self.gridLayout_au.addWidget(self.frequency_label, 5, 9,7, 7)

        self.gridLayout_au.addWidget(self.audiogramRadioButton, 12, 9,10, 7)

        self.gridLayout_12.addLayout(self.gridLayout_au, 5, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_8, 3, 2, 1, 1)

        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")

        self.originalSpectrugramLabel = QtWidgets.QLabel(self.centralwidget)
        self.originalSpectrugramLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.originalSpectrugramLabel.setObjectName("originalSpectrugramLabel")

        self.gridLayout_14.addWidget(self.originalSpectrugramLabel, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_14, 0, 3, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")

        self.frequencyDomainPlot = Graph(self.centralwidget, is_frequency_domain=True)
        self.frequencyDomainPlot.plot_widget.setMaximumSize(QtCore.QSize(550, 370))
        self.frequencyDomainPlot.plot_widget.setObjectName("frequencyDomainPlot")
        self.gridLayout_18.addWidget(self.frequencyDomainPlot.plot_widget, 2, 0, 1, 1)

        self.audiogramPlot = spectrogramPlot(self.centralwidget)
        self.audiogramPlot.setMaximumSize(QtCore.QSize(550, 370))
        self.audiogramPlot.setObjectName("frequencyDomainPlot")
        self.gridLayout_18.addWidget(self.audiogramPlot, 2, 0, 1, 1)

        self.frequencyDomainLabel = QtWidgets.QLabel(self.centralwidget)
        self.frequencyDomainLabel.setMaximumSize(QtCore.QSize(200, 50))
        self.frequencyDomainLabel.setObjectName("frequencyDomainLabel")

        self.gridLayout_18.addWidget(self.frequencyDomainLabel, 1, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_18, 1, 5, 6, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.originalSpectrugram = spectrogramPlot(self.centralwidget)
        self.originalSpectrugram.setMaximumSize(QtCore.QSize(400, 450))
        self.originalSpectrugram.setObjectName("originalSpectrugram")

        self.gridLayout.addWidget(self.originalSpectrugram, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout, 1, 3, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1916, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.originalFileLabel.setText(_translate("MainWindow", "Original File"))
        self.equalizedSpectrugramLabel.setText(_translate("MainWindow", "Equalized Spectrugram"))
        self.modeComboBox.setItemText(0, _translate("MainWindow", "Uniform Mode"))
        self.modeComboBox.setItemText(1, _translate("MainWindow", "Music"))
        self.modeComboBox.setItemText(2, _translate("MainWindow", "Animal Sounds"))
        self.modeComboBox.setItemText(3, _translate("MainWindow", "ECG Abnormalities"))
        self.selectModeLabel.setText(_translate("MainWindow", "Select Mode"))
        self.spectrugramCheckBox.setText(_translate("MainWindow", "Spectrugram"))
        self.equalizedFileLabel.setText(_translate("MainWindow", "Equalized File"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.speedUpButton.setText(_translate("MainWindow", "Speed Up"))
        self.speedDownButton.setText(_translate("MainWindow", "Speed Down"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.zoomInButton.setText(_translate("MainWindow", "Zoom In"))
        self.zoomOutButton.setText(_translate("MainWindow", "Zoom Out"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.linearScaleRadioButton.setText(_translate("MainWindow", "Linear Scale"))
        self.audiogramRadioButton.setText(_translate("MainWindow", "Audiogram"))

        self.frequency_label.setText(_translate("MainWindow", "Frequency Scale:"))
        self.originalSpectrugramLabel.setText(_translate("MainWindow", "Original Spectrugram"))
        self.frequencyDomainLabel.setText(_translate("MainWindow", "Frequency Domain"))



