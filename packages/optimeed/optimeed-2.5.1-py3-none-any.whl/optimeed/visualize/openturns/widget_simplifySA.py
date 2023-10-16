from PyQt5 import QtWidgets
from optimeed.consolidate import SensitivityAnalysis_SALib, SensitivityParameters
import numpy as np
from optimeed.core.tools import order_lists


class Widget_simplifySA(QtWidgets.QWidget):
    """This widget works using SALib and restrains the number of parameters used to perform the slave sensitivity analysis to the first N most influencials.
    Usage:
    - Instantiates the widget using the base sensitivty parameters
    - Set the slave sensitivity analysis using set_slave_SA
    - Update the slave with the selected limited number of parameters using update_SA
    """
    def __init__(self, init_SAparams):
        super().__init__()
        self.master_SA_study = SensitivityAnalysis_SALib(init_SAparams, list())
        self.master_SAparams = init_SAparams

        self.slave_SA_study = None
        self.nb_fit = 5

        # Input
        main_horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.label_dimensionality = QtWidgets.QLabel("Max number of parameters in SA: ")
        main_horizontal_layout.addWidget(self.label_dimensionality)

        self.textInput = QtWidgets.QSpinBox()
        self.textInput.setMinimum(0)
        self.textInput.setMaximum(100)
        self.textInput.setValue(3)
        self.textInput.textChanged.connect(self.set_nb_fit)

        main_horizontal_layout.addWidget(self.textInput)

        self.buttonValid = QtWidgets.QPushButton()
        self.buttonValid.clicked.connect(self.update_SA)
        self.buttonValid.setText("OK")
        main_horizontal_layout.addWidget(self.buttonValid)


    def set_nb_fit(self):
        num_variables = int(self.textInput.text())
        self.nb_fit = min(num_variables, len(self.master_SAparams.get_optivariables()))
        self.update_SA()

    def set_slave_SA(self, theSA):
        self.slave_SA_study = theSA

    def set_master_objectives(self, theObjectives):
        self.master_SA_study.set_objectives(theObjectives)

    def update_SA(self):
        ST = self.master_SA_study.get_sobol_ST()
        _, ordered_ST = order_lists(ST, list(range(len(self.master_SAparams.get_optivariables()))))
        ordered_ST.reverse()
        columns_to_extract = ordered_ST[0:self.nb_fit]

        # Get paramvalues
        init_paramvalues = np.array(self.master_SAparams.get_paramvalues())
        extracted_paramvalues = init_paramvalues[:,columns_to_extract]
        _, row_lists = np.unique(extracted_paramvalues, return_index=True, axis=0)
        row_lists = np.sort(row_lists)
        extracted_paramvalues_wo_duplicates = extracted_paramvalues[row_lists]

        # Get opti variables
        init_optivariables = self.master_SAparams.get_optivariables()
        extracted_optivariables = [init_optivariables[i] for i in columns_to_extract]

        new_sensitivity_parameters = SensitivityParameters(extracted_paramvalues_wo_duplicates, extracted_optivariables,
                                                           self.master_SAparams.get_device(), self.master_SAparams.get_M2P(), self.master_SAparams.get_charac())
        # Get objectives
        init_objectives = self.master_SA_study.theObjectives
        new_objectives = np.array(init_objectives)[row_lists]

        self.slave_SA_study.set_objectives(new_objectives)
        self.slave_SA_study.set_SA_params(new_sensitivity_parameters)

