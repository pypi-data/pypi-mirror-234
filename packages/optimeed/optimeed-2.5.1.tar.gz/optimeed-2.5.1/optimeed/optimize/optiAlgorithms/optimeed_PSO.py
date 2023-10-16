from .pyswarm import pso
from optimeed.core.tools import indentParagraph  # isNonePrintMessage, printIfShown, SHOW_ERROR, SHOW_WARNING
from .algorithmInterface import AlgorithmInterface
from optimeed.core import Option_class, Option_int, Option_dict, Option_bool, printIfShown, SHOW_INFO
from optimeed.optimize.optiAlgorithms.convergence.evolutionaryConvergence import EvolutionaryConvergence
import time


class MaxTimeTerminationCondition:
    def __init__(self, maxTime):
        super(MaxTimeTerminationCondition, self).__init__()
        self.maxTime = maxTime
        self.startingTime = time.time()

    def shouldTerminate(self):
        return time.time() - self.startingTime > self.maxTime


class ConvergenceTerminationCondition:
    def __init__(self, convergence, minrelchange_percent=0.1, nb_generation=15):
        self.minrelchange = minrelchange_percent
        self.nb_generation = nb_generation
        self.convergence = convergence

    def shouldTerminate(self):
        convergence = self.convergence
        if convergence.last_step() <= self.nb_generation:
            return False
        try:
            curr_hypervolume, _ = convergence.get_hypervolume(convergence.get_pareto_at_step(convergence.last_step()))
            last_hypervolume, _ = convergence.get_hypervolume(convergence.get_pareto_at_step(convergence.last_step() - self.nb_generation))
            rel_change = abs((curr_hypervolume - last_hypervolume)/curr_hypervolume * 100)  # percent
            printIfShown("Current hypervolume: {} Before hypervolume: {} Rel Change: {}".format(curr_hypervolume, last_hypervolume, rel_change), SHOW_INFO)
            if rel_change < self.minrelchange:
                printIfShown("terminating because converged !", SHOW_INFO)
            return rel_change < self.minrelchange
        except (IndexError, ZeroDivisionError):
            return False


class Optimeed_PSO(AlgorithmInterface, Option_class):  # Supports multiobj ... apparently
    KWARGS_ALGO = 2

    def __init__(self):
        super().__init__()
        self.maxTime = None  # set by set_maxtime
        self.theEvaluator = None  # set by set_evaluator
        self.add_option(self.KWARGS_ALGO, Option_dict("Keywords arguments to send to the optimization algorithm", {}))
        self.theConvergence = EvolutionaryConvergence()

        self.initialVectorGuess = None
        self.listOfOptimizationVariables = None
        self.terminationCondition = None
        self.array_evaluator = False

    def initialize(self, initialVectorGuess, listOfOptimizationVariables):
        self.initialVectorGuess = initialVectorGuess
        self.listOfOptimizationVariables = listOfOptimizationVariables

    def compute(self):
        # Get lower bounds and upper bounds
        lb = [optiVariable.get_min_value() for optiVariable in self.listOfOptimizationVariables]
        ub = [optiVariable.get_max_value() for optiVariable in self.listOfOptimizationVariables]

        # Run the optimization algorithm
        kwargs = dict()
        kwargs.update(self.get_option_value(self.KWARGS_ALGO))

        if self.terminationCondition is None:
            self.terminationCondition = MaxTimeTerminationCondition(self.maxTime)

        optimal_parameters, _function_value, is_feasible = pso(lb, ub, self.initialVectorGuess, self.theEvaluator, self.terminationCondition,
                                                               callback_generation=self.theConvergence.set_curr_step,
                                                               **kwargs)
        return [optimal_parameters]

    def set_evaluator(self, theEvaluator):
        self.theEvaluator = theEvaluator

    def set_terminationCondition(self, theTerminationCondition):
        self.terminationCondition = theTerminationCondition

    def set_maxtime(self, maxTime):
        self.maxTime = maxTime

    def __str__(self):
        theStr = ''
        theStr += "Custom PSO\n"
        theStr += indentParagraph(super().__str__(), indent_level=1)
        return theStr

    def get_convergence(self):
        return self.theConvergence
