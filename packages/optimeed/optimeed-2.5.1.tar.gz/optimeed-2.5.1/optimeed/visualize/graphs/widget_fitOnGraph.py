from PyQt5 import QtCore, QtWidgets
from .widget_graphsVisual import Widget_graphsVisualLite
from optimeed.core import Graphs, Data
from abc import ABCMeta, abstractmethod


class Abstract_FitOnGraph(metaclass=ABCMeta):
    @abstractmethod
    def get_xy(self, config_values):
        pass


class Widget_FitOnGraph(QtWidgets.QWidget):
    def __init__(self, base_x, base_y, theDataToFit, number_sliders=2):
        super().__init__()
        self.theDataToFit = theDataToFit

        # Create widget graphs
        self.theGraphs = Graphs()
        g1 = self.theGraphs.add_graph()
        base_data = Data(base_x, base_y, symbol=None, legend="Base data")
        data_fit = Data([], [], symbol=None, legend="Fit (configured) data")
        t1 = self.theGraphs.add_trace(g1, base_data)
        t2 = self.theGraphs.add_trace(g1, data_fit)
        self.wg_graphsvisual = Widget_graphsVisualLite(self.theGraphs, is_light=True, refresh_time=-1, highlight_last=False, linkX=False)

        # Create tune sliders
        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        main_vertical_layout.addWidget(self.wg_graphsvisual)
        # For the sliders
        horizontalLayout = QtWidgets.QHBoxLayout()
        self.sliders = list()

        for _ in range(number_sliders):
            new_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            new_slider.setMinimum(-1000)
            new_slider.setMaximum(1000)
            new_slider.setTickInterval(1)
            new_slider.valueChanged.connect(self.slider_handler)
            horizontalLayout.addWidget(new_slider)
            self.sliders.append(new_slider)
        self.layout().addLayout(horizontalLayout)
        self.slider_handler()

    def slider_handler(self):
        new_x, new_y = self.theDataToFit.get_xy([slider.value() for slider in self.sliders])
        theData = self.theGraphs.get_graph(0).get_trace(1)
        theData.set_data(new_x, new_y)
        self.theGraphs.updateChildren()

