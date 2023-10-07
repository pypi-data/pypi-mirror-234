from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


class Graph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes: Axes = self.figure.add_subplot(111)
        super(Graph, self).__init__(self.figure)
        self.map: np.matrix

    def setMap(self, map):
        self.map = map