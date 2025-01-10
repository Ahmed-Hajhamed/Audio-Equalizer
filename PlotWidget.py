import pyqtgraph as pg


class CustomPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = None 
        self.is_selecting = False
        self.start_pos = None 
        self.selection_enabled = False

        self.region = pg.LinearRegionItem(brush=(200, 50, 50, 50))
        self.region.setZValue(10)
        self.region.setRegion([0, 0])
        self.region.setVisible(False)
        self.addItem(self.region)

    def set_selection_mode(self, enabled):
        """Enable or disable selection mode."""
        self.selection_enabled = enabled
        if not enabled:
            self.region.setVisible(False)

    def mouseDoubleClickEvent(self, event):
        if event.button() == 1:
            self.is_selecting = True
            self.start_pos = self.plotItem.vb.mapSceneToView(event.pos()).x() 
            self.region.setRegion([self.start_pos, self.start_pos])
            self.region.setVisible(True)

    def mouseMoveEvent(self, event):
        if self.is_selecting and self.selection_enabled:
            current_pos = self.plotItem.vb.mapSceneToView(event.pos()).x()
            self.region.setRegion([self.start_pos, current_pos])

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_selecting and self.selection_enabled:
            self.is_selecting = False
            end_pos = self.plotItem.vb.mapSceneToView(event.pos()).x()

            if self.start_pos != end_pos:
                self.region.setRegion([min(self.start_pos, end_pos), max(self.start_pos, end_pos)])

        super().mouseReleaseEvent(event)
