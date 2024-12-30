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

class Graph():

    def __init__(self, is_frequency_domain=False, winer = False, shading= False):
        super().__init__()
        self.plot_widget = pg.PlotWidget() if winer == False else CustomPlotWidget()
        self.plot_widget.setBackground('#2E2E2E')
        self.plot_widget.setFixedHeight(200)
        self.signal = None
        self.selected_data = None
        self.current_index = 0
        self.current_index_increment = 10
        self.is_paused = False
        self.is_off = False
        self.is_frequency_domain=is_frequency_domain
        self.curve = None

        if winer:
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

    def update_plot(self):
        if self.signal is not None:
            self.curve.setData(self.signal[0], self.signal[1], pen="green")


    def play_pause(self, play_pause_button):
        if self.is_paused:
            # set_icon(play_pause_button, "icons\pause.png")
            play_pause_button.setText("PAUSE")
        else:
            # set_icon(play_pause_button, "icons/play.png")
            play_pause_button.setText("PLAY")
        self.is_paused = not self.is_paused

    def rewind_signal(self):
        pass

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
        """Set the plot limits based on the loaded data."""
        if len(self.signal[0])>0:
            x_max = self.signal[0][-1]
            y_min = min(self.signal[1])
            y_max = max(self.signal[1])

            y_min = y_min - y_min * 0.05 if y_min > 0 else y_min + y_min * 0.05

            self.plot_widget.setLimits(
                xMin=-0.1, xMax=x_max + 0.1,
                yMin=y_min, yMax=y_max + y_max * 0.05
            )
            

    def remove_old_curve(self):
        if self.curve:
            self.plot_widget.removeItem(self.curve)

    def speed_up_signal(self):
        pass
    
    def speed_down_signal(self):
        pass
    
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
    
    def reset_shading_region(self):
        self.shading_region.setRegion([0, 0])
