import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import sys
from PlotWidget import CustomPlotWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Region Selection Example")
        
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create a vertical layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create a PlotWidget
        self.plot_widget = CustomPlotWidget()
        layout.addWidget(self.plot_widget)
        
        # Plot some data
        x = list(range(100))
        y = [i**0.5 for i in x]
        self.plot_widget.plot(x, y)
        
        
        # Connect a signal to capture region changes
        self.plot_widget.region.sigRegionChanged.connect(self.region_changed)

    def region_changed(self):
        region_bounds = self.region.getRegion()  # Get the region's start and end points
        print(f"Selected region: {region_bounds}")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
