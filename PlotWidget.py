import pyqtgraph as pg


class CustomPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = None  # Placeholder for the reference to Graph
        self.is_selecting = False  # To track whether the user is selecting a region
        self.start_pos = None  # Initial mouse click position
        self.selection_enabled = False  # Tracks if selection mode is active

        # Create the region but keep it hidden initially
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.region.setRegion([0, 0])  # Initially set it to 0 width
        self.region.setVisible(False)  # Hide it initially
        self.addItem(self.region)

    def set_graph_reference(self, graph):
        """Set a reference to the Graph instance."""
        self.graph = graph
    
    def set_selection_mode(self, enabled):
        """Enable or disable selection mode."""
        self.selection_enabled = enabled
        if not enabled:
            # Hide the region if the mode is disabled
            self.region.setVisible(False)

    def mouseDoubleClickEvent(self, event):
        if not self.selection_enabled or event.button() == 2:  # Ignore right-click
            return

        if event.button() == 1:  # Handle only left-click
            # Start region selection
            self.is_selecting = True
            self.start_pos = self.plotItem.vb.mapSceneToView(event.pos()).x()  # Store the initial click position

            # Make the region visible but initially collapsed
            self.region.setRegion([self.start_pos, self.start_pos])
            self.region.setVisible(True)

        # Don't call super().mousePressEvent for left-click to avoid conflicts

    def mouseMoveEvent(self, event):
        if self.is_selecting and self.selection_enabled:
            # Dynamically update the region as the user drags the mouse
            current_pos = self.plotItem.vb.mapSceneToView(event.pos()).x()
            self.region.setRegion([self.start_pos, current_pos])

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Finish the selection
        if self.is_selecting and self.selection_enabled:
            self.is_selecting = False
            end_pos = self.plotItem.vb.mapSceneToView(event.pos()).x()

            # Ensure that the region makes sense (start < end)
            if self.start_pos != end_pos:
                self.region.setRegion([min(self.start_pos, end_pos), max(self.start_pos, end_pos)])

        super().mouseReleaseEvent(event)
