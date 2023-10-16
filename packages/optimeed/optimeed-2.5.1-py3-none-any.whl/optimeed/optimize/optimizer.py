from .characterization import Characterization
from .mathsToPhysics import MathsToPhysics
from .optiAlgorithms import MultiObjective_GA

from optimeed.core import SaveableObject
from optimeed.core import printIfShown
from optimeed.core.commonImport import SHOW_INFO
from optimeed.core.evaluators import Evaluator
from .evaluate import _evaluate, get_evaluate_args


default = dict()
default['M2P'] = MathsToPhysics
default['Charac'] = Characterization
default['Algo'] = MultiObjective_GA
default['Evaluator'] = Evaluator


class OptimizerSettings(SaveableObject):
    def __init__(self, theDevice, theObjectives, theConstraints, theOptimizationVariables,
                 theOptimizationAlgorithm=None, theMathsToPhysics=None, theCharacterization=None):
        """
        Prepare the optimizer for the optimization.

        :param theDevice: object of type  :class:`~optimeed.core.interfaceDevice.InterfaceDevice`
        :param theObjectives: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
        :param theConstraints: list of objects of type :class:`~optimeed.optimize.objAndCons.interfaceObjCons.InterfaceObjCons`
        :param theOptimizationVariables: list of objects of type :class:`~optimeed.optimize.optiVariable.OptimizationVariable`
        :param theOptimizationAlgorithm: list of objects of type :class:`~optimeed.optimize.optiAlgorithms.algorithmInterface.AlgorithmInterface`
        :param theMathsToPhysics: object of type :class:`~optimeed.optimize.mathsToPhysics.interfaceMathsToPhysics.InterfaceMathsToPhysics`
        :param theCharacterization: object of type :class:`~optimeed.optimize.characterization.interfaceCharacterization.InterfaceCharacterization`
        :return:
        """
        self.theDevice = theDevice
        self.theMathsToPhysics = theMathsToPhysics if theMathsToPhysics is not None else default['M2P']()
        self.theCharacterization = theCharacterization if theCharacterization is not None else default['Charac']()
        self.theObjectives = theObjectives
        self.theConstraints = theConstraints
        self.theOptimizationAlgorithm = theOptimizationAlgorithm if theOptimizationAlgorithm is not None else default['Algo']()
        self.theOptimizationVariables = theOptimizationVariables

    def get_additional_attributes_to_save(self):
        return ["theDevice", "theMathsToPhysics", "theCharacterization", "theOptimizationAlgorithm"]

    def get_additional_attributes_to_save_list(self):
        return ["theObjectives", "theConstraints", "theOptimizationVariables"]

    def get_device(self):
        return self.theDevice

    def get_M2P(self):
        return self.theMathsToPhysics

    def get_charac(self):
        return self.theCharacterization

    def get_optivariables(self):
        return self.theOptimizationVariables

    def get_objectives(self):
        return self.theObjectives
    
    def get_constraints(self):
        return self.theConstraints

    def get_optialgorithm(self):
        return self.theOptimizationAlgorithm


def run_optimization(optimizer_settings: OptimizerSettings, opti_historic, max_opti_time_sec=10, evaluator=None,
                     return_x_solutions=False, initial_x=None):
    """
    Perform the optimization.

    :param optimizer_settings: :class:`OptimizerSettings` containing all information in models, objectives and optimization variable
    :param opti_historic: OptiHistoric to log evaluations and results
    :param max_opti_time_sec: Maximum optimization time (default stopping criterion, unless modified in algorithm)
    :param evaluator: define how to evaluate the evaluation functions. Useful for multicore usage.
    :param return_x_solutions: If True, returns raw parameters in reults
    :param initial_x: if not None, tell the algorithm to account for the solution x to start the algorithm. Otherwise, use base device.
    :return: list of the best optimized devices, convergence information and [if return_x_solutions=True] best solutions
    """
    theOptimizationAlgorithm = optimizer_settings.get_optialgorithm()

    # Initialize opti algorithms
    if evaluator is None:
        evaluator = default['Evaluator'](optimizer_settings)

    evaluator.set_evaluation_function(_evaluate, get_evaluate_args)

    if initial_x is None:
        initial_x = optimizer_settings.get_M2P().fromPhysToMaths(optimizer_settings.get_device(),
                                                                 optimizer_settings.get_optivariables())
    # Start logging
    evaluator.add_callback(opti_historic.log_after_evaluation)  # Every evaluation => tell opti_historic

    evaluator.start()
    opti_historic.start(optimizer_settings)

    theOptimizationAlgorithm.set_maxtime(max_opti_time_sec)
    theOptimizationAlgorithm.set_evaluator(evaluator)

    # Initialize the algorithm
    theOptimizationAlgorithm.initialize(initial_x, optimizer_settings.get_optivariables())

    # Get track of convergence
    convergence = theOptimizationAlgorithm.get_convergence()
    opti_historic.set_convergence(convergence)

    # Start optimization
    printIfShown("Performing optimization", SHOW_INFO)
    x_solutions = theOptimizationAlgorithm.compute()
    printIfShown("Optimization ended", SHOW_INFO)

    # Manage results
    success, best_devices = opti_historic.get_best_devices_without_reevaluating(x_solutions)
    if not success:
        printIfShown("Could not retrieve best devices from database ... Reevaluating", SHOW_INFO)
        results = evaluator.evaluate_all(x_solutions)
        best_devices = [result['device'] for result in results]

    evaluator.close()

    # Set results and save
    opti_historic.set_results(best_devices)
    opti_historic.save()
    if not return_x_solutions:
        return best_devices, convergence

    return best_devices, convergence, x_solutions
