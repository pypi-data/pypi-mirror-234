import shutil
from abc import ABCMeta, abstractmethod
from optimeed.core import SaveableObject, AutosaveStruct, create_unique_dirname, SHOW_INFO, printIfShown, Performance_ListDataStruct, ListDataStruct
from typing import List
from .evaluate import _evaluate, get_evaluate_args
from optimeed.core import SingleObjectSaveLoad
from optimeed.core import getPath_workspace, SHOW_ERROR, order_lists
from optimeed.optimize import Real_OptimizationVariable
from optimeed.core import Evaluator
from multiprocessing import Pool
import math
import numpy as np
import os


_filename_sensitivityparams = "sensitivity_params.json"
_foldername_embarrassingly_parallel_results = "_jobs_results"
_filename_sensitivityresults = "sensitivity.json"


class SensitivityResults(SaveableObject):
    paramsToEvaluate: List[float]
    success: bool
    index: int

    def __init__(self):
        self.paramsToEvaluate = [0.0]
        self.device = None
        self.success = False
        self.index = 0

    def add_data(self, params, device, success, index):
        self.device = device
        self.success = success
        self.paramsToEvaluate = params
        self.index = index

    def get_additional_attributes_to_save(self):
        return ["device"]


class SensitivityParameters(SaveableObject):
    list_of_optimization_variables: List[Real_OptimizationVariable]
    param_values: List[List[float]]

    def __init__(self, param_values, list_of_optimization_variables, theDevice, theMathsToPhys, theCharacterization):
        """
        These are the parameters t
        :param list_of_optimization_variables: list of OptiVariables that are analyzed
        :param theDevice: /
        :param theMathsToPhys: /
        :param theCharacterization: /"""
        self.theDevice = theDevice
        self.theMathsToPhys = theMathsToPhys
        self.theCharacterization = theCharacterization
        self.list_of_optimization_variables = list_of_optimization_variables
        self.param_values = param_values

    def get_device(self):
        return self.theDevice

    def get_M2P(self):
        return self.theMathsToPhys

    def get_charac(self):
        return self.theCharacterization

    def get_optivariables(self):
        return self.list_of_optimization_variables

    def get_paramvalues(self):
        return self.param_values

    def get_additional_attributes_to_save(self):
        return ["theDevice", "theMathsToPhys", "theCharacterization"]


class Restrained_SensitivityParameters(SensitivityParameters):
    """Class to perform Sensitivty Analysis on a subset of the full parameters"""
    def __init__(self, *args):
        super().__init__(*args)
        self.selected = list()

    @staticmethod
    def create_from_sensitivityParameters(theSensitivityParameters):
        restrained_SA = Restrained_SensitivityParameters(theSensitivityParameters.get_device(), theSensitivityParameters.get_M2P(),
                                                         theSensitivityParameters.get_charac(), theSensitivityParameters.get_optivariables(), theSensitivityParameters.get_paramvalues())
        return restrained_SA

    def set_selected(self, selection):
        self.selected = selection

    def get_optivariables(self):
        init_optivariables = super().get_optivariables()
        return [init_optivariables[index] for index in self.selected]

    def get_paramvalues(self):
        init_paramvalues = super().get_paramvalues()
        return [[line[index] for index in self.selected] for line in init_paramvalues]


class SensitivityAnalysis_LibInterface(metaclass=ABCMeta):
    """Interface a library for sensitivity analysis

    :param theSensitivityParameters: :class:`optimeed.consolidate.sensitivity_analysis.SensitivityParameters`
    :param theObjectives: array-like objective associated to evaluation, using Sobol sampling"""
    def __init__(self, theSensitivityParameters: SensitivityParameters, theObjectives):
        self.theSensitivityParameters = theSensitivityParameters
        self.theObjectives = theObjectives
        self.performed = False

    @staticmethod
    @abstractmethod
    def sample_sobol(theOptimizationVariables, N):
        pass

    @abstractmethod
    def get_sobol_S1(self):
        """
        Get first order sobol indices

        :return:
        """
        pass

    @abstractmethod
    def get_sobol_S1conf(self):
        pass

    @abstractmethod
    def get_sobol_S2(self):
        """
        Get second order sobol indices

        :return:
        """
        pass

    @abstractmethod
    def get_sobol_ST(self):
        """
        Get total order sobol indices

        :return:
        """
        pass

    @abstractmethod
    def get_sobol_STconf(self):
        pass

    def get_summary(self):
        """Display a summary of the sobol indices"""
        S1 = self.get_sobol_S1()
        S1conf = self.get_sobol_S1conf()
        ST = self.get_sobol_ST()
        STconf = self.get_sobol_STconf()

        nb_params = len(self.get_SA_params().get_optivariables())
        _, ordered_S1 = order_lists(S1, list(range(nb_params)))
        _, ordered_ST = order_lists(ST, list(range(nb_params)))
        ordered_S1.reverse()
        ordered_ST.reverse()

        def format_array(permutations, S, Sconf, name):
            theStr = ''
            theStr += '─' * 120 + '\n'
            theStr += "{:^12}{:^14}{:^25}{:<}".format(*["Rank (" + name + ")", "Sobol value", "+- 95% conf", "Param name"]) + '\n'
            theStr += '─' * 120 + '\n'
            for i, map_index in enumerate(permutations):
                row = [i + 1, S[map_index], Sconf[map_index], self.get_SA_params().get_optivariables()[map_index].get_attribute_name()]
                theStr += "{:^12}{:^14.3f}{:^25.3f}{}".format(*row) + '\n'
            theStr += '─' * 50 + '\n'
            theStr += "{:^12}{:^14.3f}{:^25}{:<}".format("SUM", sum(S), "", "") + '\n'
            return theStr

        S1_array = format_array(ordered_S1, S1, S1conf, "S1")
        ST_array = format_array(ordered_ST, ST, STconf, "ST")
        print(S1_array)
        print(ST_array)

    def get_convergence_S1(self, stepsize=1):
        """
        Create dictionary for convergence plot - First order index

        :param stepsize: increments of sampling size
        :return: Dictionary
        """
        return self._get_convergence(self.get_sobol_S1, stepsize)

    def get_convergence_ST(self, stepsize=1):
        """
        Create dictionary for convergence plot - Total order index

        :param stepsize: increments of sampling size
        :return: Dictionary
        """
        return self._get_convergence(self.get_sobol_ST, stepsize)

    def _get_convergence(self, method, stepsize):
        opti_variables = self.get_SA_params().get_optivariables()
        nb_params = len(opti_variables)

        max_nb_step = math.floor(len(self.theObjectives) / (2 * nb_params + 2))

        outputs = list()
        steps = list(range(2, max_nb_step, stepsize))

        theObjectives = np.array(self.theObjectives, copy=True)

        for sample_size in steps:
            printIfShown("Doing {} over {}".format(sample_size, max_nb_step))
            self.set_objectives(np.array(theObjectives[0:sample_size * (2 * nb_params + 2)]))
            outputs.append(method())

        outputs_dict = dict()
        for i in range(nb_params):
            outputs_dict[i] = {'S': [output[i] for output in outputs],
                               'step': steps,
                               'name': opti_variables[i].get_attribute_name()}
        self.set_objectives(theObjectives)

        return outputs_dict

    def get_SA_params(self):
        return self.theSensitivityParameters

    def set_SA_params(self, theSensitivityParameters):
        self.theSensitivityParameters = theSensitivityParameters
        self.performed = False

    def set_objectives(self, theObjectives):
        self.theObjectives = theObjectives
        self.performed = False


def _find_missings(theSensitivityParameters, studyname):
    missings = list()
    for index, _ in enumerate(theSensitivityParameters.get_paramvalues()):
        saved_filename = os.path.join(getPath_workspace(), studyname, _foldername_embarrassingly_parallel_results, "{}.json".format(index))
        print(saved_filename)
        if not os.path.exists(saved_filename):
            missings.append(index)
    return missings


def prepare_embarrassingly_parallel_sensitivity(theSensitivityParameters, studyname):
    """
    Initialize sensitivity analysis folder
    :param theSensitivityParameters:
    :param studyname: Folder to be created in Workspace
    :return:
    """
    project_foldername = os.path.join(getPath_workspace(), studyname)
    foldername_tempfiles = os.path.join(project_foldername, _foldername_embarrassingly_parallel_results)
    shutil.rmtree(foldername_tempfiles, ignore_errors=True)
    os.makedirs(foldername_tempfiles)  # Also create project_foldername dir
    SingleObjectSaveLoad.save(theSensitivityParameters, os.path.join(project_foldername, _filename_sensitivityparams))
    printIfShown("Files created. There will be {} indices to evaluate".format(len(theSensitivityParameters.get_paramvalues())), SHOW_INFO)


def launch_embarrassingly_parallel_sensitivity(theSensitivityParameters, studyname, base_index, mult_factor=1):
    """
    Single job launcher for an embarrassingly parallel evaluation
    :param theSensitivityParameters:
    :param studyname: Name of the folder in Workspace in which the study is performed
    :param base_index: start index (Formula: index to evaluate = base_index*mult_factor)
    :param mult_factor: Multiplication factor of the base_index. Allows to overcome QOSMaxJobPerUserLimit in clusters.
    :return:
    """
    for offset_index in range(mult_factor):
        new_index = base_index*mult_factor + offset_index

        saved_filename = os.path.join(getPath_workspace(), studyname, _foldername_embarrassingly_parallel_results, "{}.json".format(new_index))
        if not os.path.exists(saved_filename):
            output = _evaluate(new_index, get_evaluate_args(theSensitivityParameters))
            result = encapsulate_result(output)
            SingleObjectSaveLoad.save(result, saved_filename)


def launch_missing_embarrassingly_parallel_sensitivity(theSensitivityParameters, studyname, missing_list, base_index, mult_factor=1):
    """Same as launch_embarrassingly_parallel_sensitivity, but using the 'missing_list' arg used for mapping"""
    for offset_index in range(mult_factor):
        new_index = missing_list[base_index*mult_factor + offset_index]

        saved_filename = os.path.join(getPath_workspace(), studyname, _foldername_embarrassingly_parallel_results, "{}.json".format(new_index))
        if not os.path.exists(saved_filename):
            output = _evaluate(new_index, get_evaluate_args(theSensitivityParameters))
            result = encapsulate_result(output)
            SingleObjectSaveLoad.save(result, saved_filename)


def gather_embarrassingly_parallel_sensitivity(theSensitivityParameters, studyname):
    """
    Gather the results. If some are missing, display the indices.

    :param theSensitivityParameters:
    :param studyname:
    :return:
    """
    missings = _find_missings(theSensitivityParameters, studyname)
    if len(missings):
        printIfShown("Could not gather results yet, several parameters remain unevaluated:", SHOW_ERROR)
        printIfShown("{}".format(missings), SHOW_ERROR)
        exit(-1)

    results = Performance_ListDataStruct()

    for index, _ in enumerate(theSensitivityParameters.get_paramvalues()):
        saved_filename = os.path.join(getPath_workspace(), studyname, _foldername_embarrassingly_parallel_results, "{}.json".format(index))
        with open(saved_filename, 'r') as f:
            theStr = f.read()
        results.add_json_data(theStr)
    results.save(os.path.join(getPath_workspace(), studyname, _filename_sensitivityresults))


def condition_aborted_sensitivities(foldername):
    theSensitivityParameters = SingleObjectSaveLoad.load(os.path.join(foldername, _filename_sensitivityparams))
    myDataStruct = Performance_ListDataStruct().load(os.path.join(foldername, _filename_sensitivityresults))

    max_nb_eval = len(theSensitivityParameters.param_values)
    index_SA_to_index_in_col = [None]*max_nb_eval

    for index_elem in range(myDataStruct.get_nbr_elements()):
        index_SA = myDataStruct.get_attribute_value_at_index_fast("index", index_elem)
        index_SA_to_index_in_col[int(index_SA)] = index_elem

    max_available_SA = index_SA_to_index_in_col.index(None)
    trunc_available_SA = index_SA_to_index_in_col[0:max_available_SA]
    new_col = myDataStruct.extract_collection_from_indices(trunc_available_SA)
    theSensitivityParameters.param_values = theSensitivityParameters.param_values[0:max_available_SA]

    # Save items
    save_dir = "{}_conditioned".format(foldername)
    shutil.copytree(foldername, save_dir)
    new_col.save(os.path.join(save_dir, _filename_sensitivityresults))
    SingleObjectSaveLoad.save(theSensitivityParameters, os.path.join(save_dir, _filename_sensitivityparams))
    printIfShown("Succeeded to condition SA. \n Saved directory: {} \n Number of elems before: {} \n Number of elems in SA: {} \n"
                 .format(save_dir, max_nb_eval, max_available_SA), SHOW_INFO)


def encapsulate_result(sensitivity_result):
    result = SensitivityResults()
    result.add_data(sensitivity_result["x"], sensitivity_result["device"], sensitivity_result["success"], sensitivity_result["index"])
    return result


class SensitivityHistoric:
    def __init__(self, foldername, nb_to_do):
        self.autosave_struct = AutosaveStruct(Performance_ListDataStruct(), filename=os.path.join(foldername, _filename_sensitivityresults))
        self.autosave_struct.start_autosave(timer_autosave=60*5)
        self.nb_to_do = nb_to_do
        self.nb_done = 0
        self.permutations = list()

    def add_result(self, sensitivity_result):
        self.permutations.append(sensitivity_result["index"])  # Helpful for asynchronous evaluations to order back everything
        result_encapsulated = encapsulate_result(sensitivity_result)
        self.autosave_struct.get_datastruct().add_data(result_encapsulated)

        printIfShown("did {} over {}".format(self.nb_done, self.nb_to_do), SHOW_INFO)
        self.nb_done += 1

    def task_finished(self):
        self.autosave_struct.stop_autosave()
        self.autosave_struct.get_datastruct().reorder(permutations=self.permutations)
        self.autosave_struct.save()
        return self.autosave_struct.get_datastruct()


def evaluate_sensitivities(theSensitivityParameters: SensitivityParameters, studyname="sensitivity", indices_to_evaluate=None, evaluator=None):
    """
    Evaluate the sensitivities

    :param theSensitivityParameters: class`~SensitivityParameters`
    :param studyname: Name of the study, that will be the subfolder name in workspace
    :param indices_to_evaluate: if None, evaluate all param_values, otherwise if list: evaluate subset of param_values defined by indices_to_evaluate
    :param evaluator: define how to evaluate the evaluation functions. Useful for multicore usage.
    :return: collection of class`~SensitivityResults`
    """
    # Retrieve the indices to evaluate
    if indices_to_evaluate is None:
        param_values = theSensitivityParameters.get_paramvalues()
        indices = list(range(len(param_values)))
    else:
        indices = indices_to_evaluate

    # Retrieve the evaluator
    if evaluator is None:
        evaluator = Evaluator(theSensitivityParameters)

    # Create the logs
    foldername = create_unique_dirname(os.path.join(getPath_workspace(), studyname))  # Workspace folder
    SingleObjectSaveLoad.save(theSensitivityParameters, os.path.join(foldername, _filename_sensitivityparams))  # parameters
    theSensitivityHistoric = SensitivityHistoric(foldername, len(indices))  # Results

    # Link historic with evaluator
    evaluator.add_callback(theSensitivityHistoric.add_result)
    evaluator.set_evaluation_function(_evaluate, get_evaluate_args)
    evaluator.start()
    evaluator.evaluate_all(indices)
    evaluator.close()

    # Using the historic => order everything and returns the result struct
    return theSensitivityHistoric.task_finished()


def evaluate_sensitivities_fast(theSensitivityParameters: SensitivityParameters):
    """Deactivate multicore and save management for fast results"""
    myDataStruct = ListDataStruct()
    [myDataStruct.add_data(
        encapsulate_result(_evaluate(index, get_evaluate_args(theSensitivityParameters)))
    )
        for index in range(len(theSensitivityParameters.get_paramvalues()))]
    return myDataStruct
