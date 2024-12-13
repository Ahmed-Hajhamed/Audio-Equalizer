import pyqtgraph as pg
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, QSize
import numpy as np
from PlotWidget import CustomPlotWidget

def set_icon(button, icon_path):
    pixmap = QPixmap(icon_path)
    button.setIcon(QIcon(pixmap))
    button.setIconSize(QSize(30, 30))
    button.setFixedSize(30, 30)
    button.setStyleSheet("border: none; background-color: none;")

class Graph():
    current_index = 0
    current_index_increment = 10
    timer = QTimer()
    timer.setInterval(100)  

    def __init__(self, centralWidget, is_frequency_domain=False):
        super().__init__()
        self.plot_widget = pg.PlotWidget(centralWidget) if not is_frequency_domain else CustomPlotWidget(centralWidget)
        # self.plot_widget.setFixedHeight(300)
        self.signal = None
        self.selected_data = None
        self.current_index = 0
        self.current_index_increment = 10
        self.is_paused = False
        self.is_off = False
        self.curve = None
        self.window_size = 100
        self.is_frequency_domain=is_frequency_domain
        if not self.is_frequency_domain:
            Graph.timer.timeout.connect(self.update_plot)
        else :
            print("its wrok")
            self.plot_widget.region.sigRegionChanged.connect(self.on_region_changed)

    def add_signal(self, signal, start=True, color=None):
        color = "b" if color is None else color
        self.signal = signal
        if start:
            self.curve = self.plot_widget.plot(signal[0][:1], signal[1][:1], pen=color)
        else :

            self.curve = self.plot_widget.plot(signal[0][:len(signal[0])], signal[1][:len(signal[1])], pen=color)
        self.set_plot_limits()
        if start:
            Graph.timer.start()
            # self.timer.start()

    def update_plot(self):
        if Graph.current_index < len(self.signal[0]):
            self.curve.setData(self.signal[0][:Graph.current_index], self.signal[1][:Graph.current_index])
        Graph.current_index += Graph.current_index_increment

        time = self.signal[0]
        start_index = max(0, Graph.current_index - self.window_size)
        self.plot_widget.setXRange(time[start_index], time[Graph.current_index], padding=1)
        self.plot_widget.setLimits(xMax=time[Graph.current_index])

    def play_pause(self, play_pause_button):
        if self.is_paused:
            Graph.timer.start()
            # set_icon(play_pause_button, "icons\pause.png")
            play_pause_button.setText("PAUSE")
        else:
            Graph.timer.stop()
            # set_icon(play_pause_button, "icons/play.png")
            play_pause_button.setText("PLAY")
        self.is_paused = not self.is_paused

    def rewind_signal(self):
        if len(self.signal) > 0:
            Graph.current_index = 0
            Graph.timer.start()

    def off_signal(self):
        Graph.timer.stop()
        self.current_index = 0
        self.is_paused = False
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
                xMin=0, xMax=x_max + 10,
                yMin=y_min, yMax=y_max + y_max * 0.05
            )

    def reconstruct_signal_on_equalized_plot(self, time, re_signal):
        self.remove_old_curve()
        self.signal = np.array([time, re_signal])
        if Graph.current_index < len(self.signal[0]):
            self.curve =self.plot_widget.plot(self.signal[0][:Graph.current_index],
                                              self.signal[1][:Graph.current_index], pen=(0, 0, 255))
            self.set_plot_limits()
            

    def remove_old_curve(self):
        self.plot_widget.removeItem(self.curve)

    def speed_up_signal(self):
        if Graph.current_index_increment <= 80:
            Graph.current_index_increment += 5
    
    def speed_down_signal(self):
        if Graph.current_index_increment >= 10:
            Graph.current_index_increment -= 5
    
    def on_region_changed(self):
        """Handle changes in the selected region."""
        if self.plot_widget.region:
            min_x, max_x = self.plot_widget.region.getRegion()

            signal = self.signal
            mask = (signal[0] >= min_x) & (signal[0] <= max_x)
            selected_x = signal[0][mask]
            selected_y = signal[1][mask]
            self.selected_data = np.array([selected_x, selected_y])

