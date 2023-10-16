from PyQt5 import QtWidgets
from optimeed.visualize.graphs import Widget_graphsVisualLite
from optimeed.core import Graphs, Data, SHOW_WARNING, printIfShown, SHOW_INFO
from optimeed.visualize.widgets import Widget_listWithSearch
import numpy as np


class Widget_Metamodel_PC_Tuner(QtWidgets.QWidget):
    """Class to tune a OpenTURNS Polynomial Chaos fit.
    Provides an interface to interactively select fit degree and display information about its quality"""

    def __init__(self):
        super().__init__()
        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Widget slider
        self.widget_poldegree = QtWidgets.QSpinBox()
        self.widget_poldegree.setMinimum(1)
        self.widget_poldegree.setMaximum(20)
        self.widget_poldegree.setValue(2)

        self.label_degree = QtWidgets.QLabel("Order: NA")
        self.label_Q2 = QtWidgets.QLabel("Q2: {:.5f} %".format(1.0*100))

        self.button_fit = QtWidgets.QPushButton("Fit")
        self.button_fit.clicked.connect(self.do_fit)

        self.button_copy = QtWidgets.QPushButton("Copy")
        self.button_copy.clicked.connect(self._copy_metamodel)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(self.widget_poldegree)
        horizontalLayout.addWidget(self.button_fit)
        horizontalLayout.addWidget(self.label_degree)
        horizontalLayout.addWidget(self.label_Q2)
        horizontalLayout.addWidget(self.button_copy)

        main_vertical_layout.addLayout(horizontalLayout)

        theGraphs = Graphs()
        g1 = theGraphs.add_graph(updateChildren=False)
        self.data_ideal = Data([], [], x_label='model', y_label='metamodel', legend='Ideal', is_scattered=False)
        self.data_comparison = Data([], [], x_label='model', y_label='metamodel', legend='Predicted', is_scattered=True, symbolsize=5, outlinesymbol=1)
        theGraphs.add_trace(g1, self.data_ideal, updateChildren=False)
        theGraphs.add_trace(g1, self.data_comparison, updateChildren=False)

        self.wg_graphs = Widget_graphsVisualLite(theGraphs, refresh_time=-1)
        main_vertical_layout.addWidget(self.wg_graphs)

        self.theMetamodel_PC = None  # Will contain class:`optimeed.consolidate.OpenTURNS_interface.Metamodel_PC_Openturns`
        self.show()

    def _copy_metamodel(self):
        theStr = self.theMetamodel_PC.get_metamodel_as_python_method()
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(theStr, mode=cb.Clipboard)
        printIfShown("{}\nCopied to clipboard!".format(theStr), SHOW_INFO)

    def set_metamodel_PC(self, theMetamodel_PC):
        """Set metamodel to fit

        :param theMetamodel_PC: Metamodel_PC_Openturns
        """
        self.theMetamodel_PC = theMetamodel_PC
        self.theMetamodel_PC.add_callback(self.update)  # If the metamodel is changed in external -> refresh the graphs
        self.update()

    def do_fit(self):
        self.theMetamodel_PC.set_fit_degree(self.widget_poldegree.value())
        self.update()

    def update(self):
        self.widget_poldegree.setValue(self.theMetamodel_PC.degree_fitted)
        if self.theMetamodel_PC is None:
            printIfShown("Please use method set_metamodel_PC before!", SHOW_WARNING)
            return
        Q2, outputs_real, outputs_model = self.theMetamodel_PC.check_goodness_of_fit()

        min_value = min(list(outputs_real) + list(outputs_model))
        max_value = max(list(outputs_real) + list(outputs_model))
        self.data_ideal.set_data([min_value, max_value], [min_value, max_value])
        self.data_comparison.set_data(outputs_real, outputs_model)
        self.label_Q2.setText("Q2: {:.5f} %".format(Q2*100))
        self.label_degree.setText("Order: {}".format(self.theMetamodel_PC.degree_fitted))
        self.wg_graphs.update_graphs()


class Widget_Metamodel_PC_Monotonicity(QtWidgets.QWidget):
    """Provides an interface to visualize the impact of a single parameter.
    The other parameters are frozen using their central point."""

    def __init__(self):
        super().__init__()
        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Create widgets
        self.listWithSearch = Widget_listWithSearch()
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_graphs)

        theGraphs = Graphs()
        g1 = theGraphs.add_graph(updateChildren=False)
        self.data_monotonicity = Data([], [], x_label='_', y_label='_', is_scattered=False)
        theGraphs.add_trace(g1, self.data_monotonicity, updateChildren=False)
        self.wg_graphs = Widget_graphsVisualLite(theGraphs, refresh_time=-1)

        main_vertical_layout.addWidget(self.listWithSearch)
        main_vertical_layout.addWidget(self.wg_graphs)

        self.theMetamodel_PC = None
        self.objectiveName = ""
        self.show()

    def set_metamodel_PC(self, theMetamodel_PC, objectiveName):
        self.theMetamodel_PC = theMetamodel_PC
        self.objectiveName = objectiveName
        self.listWithSearch.set_list([variable.get_attribute_name() for variable in self.theMetamodel_PC.inputs_as_optivariables])
        self.theMetamodel_PC.add_callback(self.update_graphs)  # If the metamodel is changed in external -> refresh the graphs
        self.update_graphs()

    def _generate_points(self,name_selected, N=100):
        """Generate points along variant selected attribute, with others fixed"""
        opti_variables = self.theMetamodel_PC.inputs_as_optivariables

        array = list()
        theLine = list()
        for variable in opti_variables:
            if variable.get_attribute_name() == name_selected:
                min_value = variable.get_min_value()
                max_value = variable.get_max_value()
                line = np.linspace(min_value, max_value, N)
                theLine = line
            else:
                middle_interval = (variable.get_min_value() + variable.get_max_value())/2
                line = [middle_interval]*N
            array.append(line)
        return np.array(array).transpose(), theLine

    def update_graphs(self):
        try:
            name_selected = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        inputs, theLine = self._generate_points(name_selected)
        outputs = self.theMetamodel_PC.evaluate_metamodel(inputs)
        self.data_monotonicity.set_data(theLine, outputs)
        self.data_monotonicity.set_kwargs({"x_label": str(name_selected), "y_label": str(self.objectiveName)})
        self.wg_graphs.update_graphs()


class Widget_Collection_Metamodels(QtWidgets.QWidget):
    """Higher level widget to tune :class:`optimeed.consolidate.OpenTURNS_interface.name_collection`.

    Embeds the underlying Widget_Metamodel_PC_Tuner and Widget_Metamodel_PC_Monotonicity."""
    def __init__(self, collection_metamodels):
        super().__init__()
        # Window split Left-right:
        # Left: Tuning
        # Right: Check monotonicity
        main_horizontal_layout = QtWidgets.QHBoxLayout(self)

        # Layout tuning
        layout_tuning = QtWidgets.QVBoxLayout()
        main_horizontal_layout.addLayout(layout_tuning)

        self.collection_metamodels = collection_metamodels
        self.collection_metamodels.add_callback(self.update_available_attributes)

        self.listWithSearch = Widget_listWithSearch()
        layout_tuning.addWidget(self.listWithSearch)

        self.wg_metamodel_PC_Tuner = Widget_Metamodel_PC_Tuner()
        layout_tuning.addWidget(self.wg_metamodel_PC_Tuner)

        # Layout monotonicity
        self.wg_metamodel_PC_Monotonicity = Widget_Metamodel_PC_Monotonicity()
        main_horizontal_layout.addWidget(self.wg_metamodel_PC_Monotonicity)
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_monotonicity_windows)

        # Manage cross-couplings
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_tune_window)  # When changed the selected attribute -> change the metamodel

        # Updates
        self.update_available_attributes()

    def update_available_attributes(self):
        self.listWithSearch.set_list(self.collection_metamodels.get_fitted_attributes())

    def update_tune_window(self):
        try:
            attribute_name = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        theMetamodel_PC = self.collection_metamodels.get_metamodel(attribute_name)
        self.wg_metamodel_PC_Tuner.set_metamodel_PC(theMetamodel_PC)

    def update_monotonicity_windows(self):
        try:
            attribute_name = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        theMetamodel_PC_Openturns = self.collection_metamodels.get_metamodel(attribute_name)
        self.wg_metamodel_PC_Monotonicity.set_metamodel_PC(theMetamodel_PC_Openturns, attribute_name)
