import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic
from optimeed.core.tools import get_recursive_attrs, order_lists
from optimeed.consolidate import SensitivityAnalysis_LibInterface
from optimeed.visualize.process_mainloop import start_qt_mainloop
import os
from optimeed.core import default_palette, Graphs, Data, printIfShown, SHOW_INFO, getPath_workspace
from optimeed.visualize.graphs.pyqtgraph import TextItem
from optimeed.visualize.graphs.widget_graphsVisual import Widget_graphsVisual
from optimeed.visualize.mainWindow import MainWindow
from PyQt5.Qt import QFont
import numpy as np


def analyse_sobol_plot_convergence(theDict, title="", hold=True):
    """Plot convergence of the sobol indices.

    :param theDict: Dictionary containing sobol indices
    :param title: Title of the convergence window
    :param hold: If true, this function will be blocking (otherwise use start_qt_mainloop)
    :return: window containing convergence graphs
    """
    theGraphs = Graphs()
    font = QFont("Arial", 10)

    palette = default_palette(len(theDict))

    g1 = theGraphs.add_graph()
    myWidgetGraphsVisuals = Widget_graphsVisual(theGraphs, highlight_last=False, refresh_time=-1, is_light=True)
    for index, key in enumerate(theDict):
        color = palette[index]

        x = theDict[key]['step']
        y1 = theDict[key]['S']
        theGraphs.add_trace(g1, Data(x, y1, symbol=None, x_label="Sample size", y_label="Sobol indices", color=color, xlim=[0, x[-1]*1.2]))
        myText = TextItem(theDict[key]['name'], color=color, anchor=(0, 0.5))
        myText.setPos(x[-1], y1[-1])
        myText.setFont(font)
        myText.setParentItem(myWidgetGraphsVisuals.get_graph(g1).theWGPlot.vb)
        myWidgetGraphsVisuals.get_graph(g1).add_feature(myText)
        myWidgetGraphsVisuals.get_graph(g1).set_title(title)
    myWindow = MainWindow([myWidgetGraphsVisuals])  # A Window (that will contain the widget)
    myWindow.run(hold)
    return myWindow


def analyse_sobol_plot_indices(SA_library: SensitivityAnalysis_LibInterface, title='', hold=True):
    """¨Plot first and total order sobol indices.

    :param SA_library: The library used for computing the sobol indices
    :param title: Title of the window
    :param hold: If true, this function will be blocking (otherwise use plt.show())
    :return:
    """
    nb_params = len(SA_library.get_SA_params().get_optivariables())
    S1 = SA_library.get_sobol_S1()
    ST = SA_library.get_sobol_ST()
    S1conf = SA_library.get_sobol_S1conf()
    STconf = SA_library.get_sobol_STconf()

    _, ordered_S1 = order_lists(S1, list(range(nb_params)))
    _, ordered_ST = order_lists(ST, list(range(nb_params)))
    ordered_S1.reverse()
    ordered_ST.reverse()

    order = ordered_ST

    # width of the bars
    barWidth = 0.3

    bars1 = [S1[map_index] for map_index in order]
    bars2 = [ST[map_index] for map_index in order]
    yer1 = [S1conf[map_index] for map_index in order]
    yer2 = [STconf[map_index] for map_index in order]

    labels = [SA_library.get_SA_params().get_optivariables()[map_index].get_attribute_name() for map_index in order]
    indices = list(range(len(bars1)))
    # labels = indices
    r1 = [x - barWidth/2 for x in indices]
    r2 = [x + barWidth/2 for x in indices]

    def split_labels(label_str, level=2):
        splitted = label_str.split('.')
        try:
            return '.'.join(splitted[-level:])
        except IndexError:
            return label_str
    plt.figure()
    plt.bar(r1, bars1, width=barWidth, color='blue', edgecolor='black', yerr=yer1, capsize=7, label='First index (S1)')
    plt.bar(r2, bars2, width=barWidth, color='cyan', edgecolor='black', yerr=yer2, capsize=7, label='Total index (ST)')
    plt.xticks(indices, map(split_labels, labels), rotation=30, ha="right")
    plt.ylabel('Sobol Index')
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.show(block=hold)


def analyse_sobol_plot_2ndOrder_indices(SA_library: SensitivityAnalysis_LibInterface, title='', hold=True):
    """¨Plot second order sobol indices. Args and kwargs are the same as analyse_sobol_plot_indices"""
    nb_params = len(SA_library.get_SA_params().get_optivariables())
    S2 = SA_library.get_sobol_S2()

    names = [var.get_attribute_name() for var in SA_library.get_SA_params().get_optivariables()]

    fig, ax = plt.subplots()
    im = ax.imshow(S2, cmap="Blues")
    cbar = ax.figure.colorbar(im, ax=ax)

    # Show all ticks and label them with the respective list entries
    slope = (4-12)/(75-25)
    offset = 12-slope*25
    max_len = max([len(word) for word in names])
    fontsize = max(6, int(max_len*slope + offset))
    fontsize = min(12, fontsize)

    ax.set_xticks(np.arange(nb_params), labels=names)
    ax.set_yticks(np.arange(nb_params), labels=names)
    plt.tick_params(axis='both', which='major', labelsize=fontsize)

    # # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=70, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(names)):
        for j in range(len(names)):
            max_value = np.nanmax(S2)
            curr_value_relative = max(0, S2[i, j]/max_value)
            color = "white" if curr_value_relative > 0.7 else "black"
            text = ax.text(j, i, "{:.3f}".format(S2[i, j]),
                           ha="center", va="center", color=color)

    ax.set_title(title)
    fig.tight_layout()
    plt.show(block=hold)


class SensitivityDisplayer(QtWidgets.QMainWindow):
    """GUI to display a sensitivity analysis."""
    def __init__(self, theLibrary: type(SensitivityAnalysis_LibInterface)):
        super().__init__()  #
        self.SA_library = theLibrary

        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'displaySensitivity_gui.ui'), self)

        self.studies = list()
        self.curr_study = None

        self.combo_collection.currentIndexChanged.connect(self._set_study)
        # Todo
        self.button_get_S1_conv.clicked.connect(self._get_S1_conv)
        self.button_get_ST_conv.clicked.connect(self._get_ST_conv)
        self.button_get_indices.clicked.connect(self._get_sobol_indices)
        self.button_export.clicked.connect(self._export)

        self.show()
        self.initialized = False
        self._windowsHolder = list()

    def add_study(self, theCollection, theParameters, name):
        """Add sensitivity study to the GUI

        :param theCollection: Results of the sensitivity study
        :param theParameters: Parameters of the sensitivity study
        :param name: Name (for the GUI) of the sensitivity study
        :return:
        """
        self.studies.append((theCollection, theParameters, name))
        self.combo_collection.addItem(name)
        if not self.initialized:
            self.combo_collection.setCurrentIndex(0)
            self.initialized = True

    def _set_study(self, index):
        self.curr_study = self.studies[index]
        first_data = self.curr_study[0].get_data_at_index(0)
        self.list_attributes.set_list(get_recursive_attrs(first_data))

    def _get_sobol_indices(self):
        curr_SA, name, objective_selected = self._curr_SA()
        analyse_sobol_plot_indices(curr_SA, title="{} | {}".format(name, objective_selected), hold=False)
        analyse_sobol_plot_2ndOrder_indices(curr_SA, title="{} | {}".format(name, objective_selected), hold=False)

    def _get_S1_conv(self):
        curr_SA, name, objective_selected = self._curr_SA()
        win = analyse_sobol_plot_convergence(curr_SA.get_convergence_S1(stepsize=10), title="S1 | {} | {}".format(name, objective_selected), hold=False)
        self._windowsHolder.append(win)

    def _get_ST_conv(self):
        curr_SA, name, objective_selected = self._curr_SA()
        win = analyse_sobol_plot_convergence(curr_SA.get_convergence_ST(stepsize=10), title="ST | {} | {}".format(name, objective_selected), hold=False)
        self._windowsHolder.append(win)

    def _curr_SA(self):
        collection, parameters, name = self.curr_study
        objective = self.get_attribute_selected()
        return self.get_SA(parameters, collection.get_list_attributes(objective)), name, objective

    def _export(self):
        curr_SA, name, objective_selected = self._curr_SA()
        S2 = np.array(curr_SA.get_sobol_S2())
        S1 = np.array(curr_SA.get_sobol_S1())
        ST = np.array(curr_SA.get_sobol_ST())
        np.fill_diagonal(S2, S1)
        base_name = "{}_{}".format(name, objective_selected)
        base_name = base_name.replace('.', '_')
        base_name = base_name.replace(' ', '_')
        np.savetxt(os.path.join(getPath_workspace(), "{}_S2.txt".format(base_name)), S2)
        np.savetxt(os.path.join(getPath_workspace(), "{}_ST.txt".format(base_name)), ST)
        printIfShown("Matrices saved in Workspace, under base_name {}".format(base_name), SHOW_INFO)

    def get_SA(self, theParameters, theObjectives):
        return self.SA_library(theParameters, theObjectives)

    def set_SA(self, theSA):
        self.SA_library = theSA

    def get_attribute_selected(self):
        return self.list_attributes.get_name_selected()

    @staticmethod
    def run():
        start_qt_mainloop()
