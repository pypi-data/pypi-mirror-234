from optimeed.core.collection import AutosaveStruct, ListDataStruct, Performance_ListDataStruct, SingleObjectSaveLoad
from optimeed.core.tools import create_unique_dirname, getPath_workspace, indentParagraph
from optimeed.core.ansi2html import Ansi2HTMLConverter
from typing import List
import numpy as np
import os
import time


class OptiHistoric:
    """Contains all the points that have been evaluated"""

    class _pointData:
        time: float
        objectives: List[float]
        constraints: List[float]

        def __init__(self, currTime, objectives, constraints):
            self.time = currTime
            self.objectives = objectives
            self.constraints = constraints

    class _LogParams:  # Keep track of evaluated parameters
        def __init__(self):
            self.params = None
            self.curr_row = 0

        def add_parameters(self, params):
            if self.params is None:
                self.params = np.zeros((int(1e6), len(params)))

            try:
                self.params[self.curr_row, :] = params[:]
            except IndexError:
                self.params = np.vstack((self.params, np.zeros((int(1e6), len(params)))))
                self.params[self.curr_row, :] = params[:]

            self.curr_row += 1

        def get_rows_indices(self, list_of_params):
            truncated_matrix = self.params[:self.curr_row+1, :]
            list_of_indices = []
            for params in list_of_params:
                try:
                    index = np.where(np.all(truncated_matrix == np.array(params), axis=1))[0][0]
                    list_of_indices.append(index)
                except IndexError:
                    return False, list_of_indices
            return True, list_of_indices

    def __init__(self, optiname="opti", autosave_timer=60*5, autosave=True, create_new_directory=True, performance_datastruct=True, folder=getPath_workspace()):
        super().__init__()
        self.start_time = 0

        foldername = "{}/{}".format(folder, optiname)
        if create_new_directory:
            foldername = create_unique_dirname(foldername)
        self.foldername = foldername

        if performance_datastruct:
            self.log_devices = AutosaveStruct(Performance_ListDataStruct(), filename=os.path.join(self.foldername, "autosaved"))
        else:
            self.log_devices = AutosaveStruct(ListDataStruct(compress_save=False), filename=os.path.join(self.foldername, "autosaved"))
        self.log_opti = AutosaveStruct(ListDataStruct(compress_save=True), filename=os.path.join(self.foldername, "logopti"))
        self.log_convergence = AutosaveStruct(ListDataStruct(compress_save=False), filename=os.path.join(self.foldername, "optiConvergence"))
        self.log_params = self._LogParams()

        if autosave:
            self.log_devices.start_autosave(autosave_timer)
            self.log_opti.start_autosave(autosave_timer)
            self.log_convergence.start_autosave(autosave_timer)

        self.autosave = autosave
        self.results = AutosaveStruct(ListDataStruct(compress_save=True), filename=os.path.join(self.foldername, "results"))

    def log_after_evaluation(self, returned_values: dict):
        """Save the output of evaluate to optiHistoric. This function should be called by the optimizer IN a process safe context."""
        self.log_params.add_parameters(returned_values["params"])
        self.log_devices.get_datastruct().add_data(returned_values["device"])
        self.log_opti.get_datastruct().add_data(self._pointData(returned_values["time"]-self.start_time, returned_values["objectives"], returned_values["constraints"]))

    def set_results(self, devicesList):
        self.results.get_datastruct().set_data(devicesList)

    def get_best_devices_without_reevaluating(self, list_of_best_params):
        success, indices_results = self.log_params.get_rows_indices(list_of_best_params)
        solutions = [self.log_devices.get_datastruct().get_data_at_index(index) for index in indices_results]
        return success, solutions

    def set_convergence(self, theConvergence):
        self.log_convergence.get_datastruct().set_data([theConvergence])

    def save(self):
        if self.autosave:
            for struct in [self.log_devices, self.log_opti, self.log_convergence, self.results]:
                struct.stop_autosave()
                struct.save()

    def get_convergence(self):
        """ :return: convergence :class:`~optimeed.optimize.optiAlgorithms.convergence.interfaceConvergence.InterfaceConvergence` """
        return self.log_convergence.get_datastruct()

    def get_devices(self):
        """ :return: List of devices (ordered by evaluation number) """
        return self.log_devices.get_datastruct()

    def get_logopti(self):
        """:return: Log optimization (to check the convergence) """
        return self.log_opti.get_datastruct()

    def start(self, optimization_parameters):
        """Function called upon starting the optimization. Create folders."""
        self.start_time = time.time()

        if self.autosave:
            SingleObjectSaveLoad.save(optimization_parameters, os.path.join(self.foldername, "optimization_parameters.json"))

            # Create summary file
            optimization_info = ''
            optimization_info += '--------------------------------------------------------------------\n'
            optimization_info += 'OBJECTIVES:\n'
            for objective in optimization_parameters.get_objectives():
                optimization_info += indentParagraph("• {} | {}".format(objective, type(objective)), indent_level=1)

            optimization_info += 'CONSTRAINTS:\n'
            for constraint in optimization_parameters.get_constraints():
                optimization_info += indentParagraph("• {} | {}".format(constraint, type(constraint)), indent_level=1)

            optimization_info += 'OPTIMIZATION VARIABLES :\n'
            for optiVariable in optimization_parameters.get_optivariables():
                optimization_info += indentParagraph('• ' + str(optiVariable), indent_level=1)

            optimization_info += 'OPTIMIZATION ALGORITHM:\n'
            optimization_info += indentParagraph("{} | {}".format(optimization_parameters.get_optialgorithm(), type(optimization_parameters.get_optialgorithm())), indent_level=1)

            optimization_info += 'CHARACTERIZATION SCHEME:\n'
            optimization_info += indentParagraph("{} | {}".format(optimization_parameters.get_charac(), type(optimization_parameters.get_charac())), indent_level=1)

            optimization_info += 'M2P:\n'
            optimization_info += indentParagraph("{} | {}".format(optimization_parameters.get_M2P(), type(optimization_parameters.get_M2P())), indent_level=1)

            with open(self.foldername + "/summary.html", 'w', encoding='utf-8') as myFile:
                conv = Ansi2HTMLConverter(dark_bg=True)
                myFile.write(conv.convert(optimization_info))


class OptiHistoric_Fast:
    """Almost empty struct, just enough to display the graphs. Used to speed up optimization"""
    def __init__(self, optiname="opti"):
        self.start_time = 0
        self.log_opti = ListDataStruct()
        foldername = "{}/{}".format(getPath_workspace(), optiname)
        os.makedirs(os.path.abspath(foldername), exist_ok=True)
        self.filename_save = "{}/{}".format(foldername, "results")

    def log_after_evaluation(self, returned_values: dict):
        self.log_opti.add_data(OptiHistoric._pointData(returned_values["time"]-self.start_time, returned_values["objectives"], returned_values["constraints"]))

    def set_results(self, theResults):
        theDataStruct = ListDataStruct()
        theDataStruct.set_data(theResults)
        theDataStruct.save(self.filename_save)

    def get_best_devices_without_reevaluating(self, _):
        return False, list()

    def set_convergence(self, theConvergence):
        pass

    def save(self):
        pass  # Done in set_results

    def get_convergence(self):
        return None

    def get_devices(self):
        return None

    def get_logopti(self):
        return self.log_opti

    def start(self, _):
        self.start_time = time.time()


class OptiHistoric_Empty:
    """Totally empty struct, cannot be used within visualization"""
    def __init__(self):
        pass

    def log_after_evaluation(self, returned_values: dict):
        pass

    def set_results(self, theResults):
        pass

    def get_best_devices_without_reevaluating(self, _):
        return False, list()

    def set_convergence(self, _):
        pass

    def save(self):
        pass

    def get_convergence(self):
        return None

    def get_devices(self):
        return None

    def get_logopti(self):
        return None

    def start(self, _):
        pass
