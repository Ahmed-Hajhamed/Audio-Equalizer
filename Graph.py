import pyqtgraph as pg
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import  QSize
import numpy as np
from PlotWidget import CustomPlotWidget

def set_icon(button, icon_path):
    pixmap = QPixmap(icon_path)
    button.setIcon(QIcon(pixmap))
    button.setIconSize(QSize(30, 30))
    button.setFixedSize(30, 30)
    button.setStyleSheet("border: none; background-color: none;")

class Graph:
    def __init__(self, wiener = False, shading= False):
        super().__init__()
        self.plot_widget = pg.PlotWidget() if wiener == False else CustomPlotWidget()
        self.plot_widget.setBackground('#2E2E2E')
        self.plot_widget.setFixedHeight(200)
        self.signal = None
        self.selected_data = None
        self.curve = None

        if wiener:
            self.plot_widget.region.sigRegionChanged.connect(self.on_region_changed)

        if shading:
            self.shading_region = pg.LinearRegionItem([0, 0], brush=(50, 50, 200, 50),pen="r")
            self.shading_region.setMovable(False)
            self.plot_widget.addItem(self.shading_region)

    def add_signal(self, signal, color=None):
        if signal is not None:
            color = "b" if color is None else color
            self.signal = signal
            self.plot_widget.removeItem(self.curve)
            self.curve = self.plot_widget.plot(signal[0], signal[1], pen=color)        
            self.set_plot_limits()

    def off_signal(self):
        self.graph_1.setLimits(xMin=0, xMax=2, yMin=-2, yMax=2)

    def zoom_in(self):
        x_range = self.plot_widget.viewRange()[0]
        y_range = self.plot_widget.viewRange()[1]

        self.plot_widget.setXRange(x_range[0] + 0.1 * (x_range[1] - x_range[0]),
                                   x_range[1] - 0.1 * (x_range[1] - x_range[0]), padding=0)
        self.plot_widget.setYRange(y_range[0] + 0.1 * (y_range[1] - y_range[0]),
                                   y_range[1] - 0.1 * (y_range[1] - y_range[0]), padding=0)
        
    def zoom_out(self):
        x_range = self.plot_widget.viewRange()[0]
        y_range = self.plot_widget.viewRange()[1]

        self.plot_widget.setXRange(x_range[0] - 0.1 * (x_range[1] - x_range[0]),
                                   x_range[1] + 0.1 * (x_range[1] - x_range[0]), padding=0)
        self.plot_widget.setYRange(y_range[0] - 0.1 * (y_range[1] - y_range[0]),
                                   y_range[1] + 0.1 * (y_range[1] - y_range[0]), padding=0)

    def set_plot_limits(self):
        if len(self.signal[0]) > 0:
            x_max = truncate_to_3_decimals(self.signal[0][-1]) # Take 3 decimals to wrap warning in plot widget
            y_min = truncate_to_3_decimals(min(self.signal[1]))
            y_max = truncate_to_3_decimals(max(self.signal[1]))

            y_min = y_min - y_min * 0.2 if y_min > 0 else y_min + y_min * 0.2

            self.plot_widget.setLimits(xMin = -0.5, xMax = 1.1 * x_max,
                yMin = 1.2 * y_min, yMax = 1.2 * y_max)
            
    def on_region_changed(self):
        """Handle changes in the selected region."""
        if self.plot_widget.region:
            min_x, max_x = self.plot_widget.region.getRegion()
            signal = self.signal
            mask = (signal[0] >= min_x) & (signal[0] <= max_x)
            selected_x = signal[0][mask]
            selected_y = signal[1][mask]
            self.selected_data = np.array([selected_x, selected_y])
    
    def update_shading_region(self, value):
        """Update playback line and shading region."""
        current_time = value/1000
        self.shading_region.setRegion([0, current_time])

def truncate_to_3_decimals(number):
    return int(number * 1000) / 1000