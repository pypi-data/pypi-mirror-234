import time
from multiprocessing import Pool, cpu_count

from optimeed.core.tools import printIfShown, SHOW_INFO, SHOW_WARNING, indentParagraph
from optimeed.optimize.optiVariable import Binary_OptimizationVariable, Integer_OptimizationVariable, Real_OptimizationVariable
from optimeed.core import Option_class, Option_int, Option_str, Option_dict
from .algorithmInterface import AlgorithmInterface
from .convergence import EvolutionaryConvergence
# Platypus imports
from .platypus import FixedLengthArray, Generator, Solution
from .platypus.algorithms import NSGAIII, SPEA2, SMPSO, NSGAII, OMOPSO, GeneticAlgorithm, GDE3
from .platypus.core import Problem, TerminationCondition, nondominated, unique
from .platypus.evaluator import Evaluator, run_job
from .platypus.operators import CompoundOperator, SBX, HUX, PM, BitFlip, DifferentialEvolution
from .platypus.types import Real, Integer, Binary
import os


class MyProblem(Problem):
    """Automatically sets the optimization problem"""

    def __init__(self, theOptimizationVariables, nbr_objectives, nbr_constraints):
        super(MyProblem, self).__init__(len(theOptimizationVariables), nbr_objectives, nbr_constraints)

        # Convert types of optimization variables
        for i in range(len(self.types)):
            optimizationVariable = theOptimizationVariables[i]
            if type(optimizationVariable) is Real_OptimizationVariable:
                self.types[i] = Real(optimizationVariable.get_min_value(), optimizationVariable.get_max_value())
            elif type(optimizationVariable) is Integer_OptimizationVariable:
                self.types[i] = Integer(optimizationVariable.get_min_value(), optimizationVariable.get_max_value())
            elif type(optimizationVariable) is Binary_OptimizationVariable:
                self.types[i] = Binary(1)
            else:
                raise ValueError("Optimization variable not managed with this algorithm")

        self.constraints[:] = "<=0"
        self.directions = FixedLengthArray(nbr_objectives, self.MINIMIZE)

    def __call__(self, solution):
        """We break the workflow philosophy of platypus: Problem does not contain the evaluation function anymore. We let the PlatypusToOptimeed_Evaluator do it"""
        raise NotImplementedError("Should not be called directly. Use PlatypusToOptimeed_Evaluator instead")

    def evaluate(self, solution):
        """We break the workflow philosophy of platypus: Problem does not contain the evaluation function anymore. We let the PlatypusToOptimeed_Evaluator do it"""
        raise NotImplementedError("Should not be called directly. Use PlatypusToOptimeed_Evaluator instead")


class PlatypusToOptimeed_Evaluator(Evaluator):
    def __init__(self, optimeedEvaluator):
        super().__init__()
        self.optimeedEvaluator = optimeedEvaluator

    def evaluate_all(self, jobs, **kwargs):
        """This weird function interfaces platypus (check "core.py", classes Algorithm, Problem, Solution)
        The normal workflow of platypus is: each solution embeds the problem, that embeds the evaluation function. A job = a solution to compute
        To compute a solution:
        -> problem.__call__(solution)
        --> decode variables
        --> call evaluation function (=Problem.evaluate) with decoded variables => get objectives and constraints
        --> encode variables
        --> fill in
        Now we let optimeed manage the multithread
        => we decode all solutions
        => call evaluate function using optimeed Evaluator (possibly parallel = fork)
        => fill all solutions for platypus
        """

        # For each solution => replace function "__call__" of problem as defined in platypus
        all_x_to_evaluate = [[job.solution.problem.types[i].decode(job.solution.variables[i]) for i in range(job.solution.problem.nvars)] for job in jobs]
        all_results = self.optimeedEvaluator.evaluate_all(all_x_to_evaluate)  # Here we fork if multithread

        for job, optimeed_result in zip(jobs, all_results):
            platypus_solution = job.solution

            problem = platypus_solution.problem
            platypus_solution.objectives[:] = optimeed_result["objectives"]
            platypus_solution.constraints[:] = optimeed_result["constraints"]
            platypus_solution.variables[:] = [problem.types[i].encode(platypus_solution.variables[i]) for i in range(problem.nvars)]
            platypus_solution.constraint_violation = sum([abs(f(x)) for (f, x) in zip(platypus_solution.problem.constraints, platypus_solution.constraints)])
            platypus_solution.feasible = platypus_solution.constraint_violation == 0.0
            platypus_solution.evaluated = True
        return jobs


class MyGenerator(Generator):
    """Population generator to insert initial individual"""

    def __init__(self, initialVectorGuess):
        super(MyGenerator, self).__init__()
        self.initialVectorGuess = initialVectorGuess
        self.inserted_initialVector = False

    def generate(self, problem):
        solution = Solution(problem)
        if not self.inserted_initialVector:
            solution.variables = [x.encode(self.initialVectorGuess[i]) for i, x in enumerate(problem.types)]
            self.inserted_initialVector = True
        else:
            solution.variables = [x.rand() for x in problem.types]
        return solution


class MaxTimeTerminationCondition(TerminationCondition):
    def __init__(self, maxTime):
        super(MaxTimeTerminationCondition, self).__init__()
        self.maxTime = maxTime
        self.startingTime = None

    def initialize(self, algorithm):
        self.startingTime = time.time()

    def shouldTerminate(self, algorithm):
        return time.time() - self.startingTime > self.maxTime


class ManualStopFromFileTermination(TerminationCondition):
    def __init__(self, filename):
        """Stops the optimization once specified filename exists.
        Usage example: ManualStopFromFileTermination(os.path.join(theOptiHistoric.foldername, 'stop.txt'))
        Do not forget to add it using :meth:`MultiObjective_GA.add_terminationCondition`
        """
        super().__init__()
        self.filename = filename

    def shouldTerminate(self, algorithm):
        return os.path.exists(self.filename)


class ConvergenceTerminationCondition(TerminationCondition):
    def __init__(self, minrelchange_percent=0.1, nb_generation=15):
        super(ConvergenceTerminationCondition, self).__init__()
        self.minrelchange = minrelchange_percent
        self.nb_generation = nb_generation

    def initialize(self, algorithm):
        pass

    def shouldTerminate(self, algorithm):
        convergence = algorithm.convergence
        if convergence.last_step() <= self.nb_generation:
            return False
        try:
            curr_hypervolume, _ = convergence.get_hypervolume(convergence.get_pareto_at_step(convergence.last_step()))
            last_hypervolume, _ = convergence.get_hypervolume(convergence.get_pareto_at_step(convergence.last_step() - self.nb_generation))
            if curr_hypervolume == last_hypervolume == 0:
                return True
            rel_change = abs((curr_hypervolume - last_hypervolume)/curr_hypervolume * 100)  # percent
            printIfShown("Current hypervolume: {} Before hypervolume: {} Rel Change: {}".format(curr_hypervolume, last_hypervolume, rel_change), SHOW_INFO)
            if rel_change < self.minrelchange:
                printIfShown("terminating because converged !", SHOW_INFO)
            return rel_change < self.minrelchange
        except (IndexError, ZeroDivisionError):
            return False


class SeveralTerminationCondition(TerminationCondition):
    def __init__(self):
        super().__init__()
        self.listOfTerminationConditions = list()

    def initialize(self, algorithm):
        for terminationCondition in self.listOfTerminationConditions:
            terminationCondition.initialize(algorithm)

    def add(self, theTerminationCondition):
        if isinstance(theTerminationCondition, TerminationCondition):
            self.listOfTerminationConditions.append(theTerminationCondition)
        else:
            printIfShown("Invalid termination condition", SHOW_WARNING)

    def shouldTerminate(self, algorithm):
        return any([terminationCondition.shouldTerminate(algorithm) for terminationCondition in self.listOfTerminationConditions])


class MultiObjective_GA(AlgorithmInterface, Option_class):
    """Based on `Platypus Library <https://platypus.readthedocs.io/en/docs/index.html>`_.
    Workflow:
    Define what to optimize and which function to call with a :class:`Problem`
    Define the initial population with a :class:`Generator`
    Define the algorithm. As options, define how to evaluate the elements with a :class:`Evaluator`, i.e., for multiprocessing.
    Define what is the termination condition of the algorithm with :class:`TerminationCondition`. Here, termination condition is a maximum time.
    """
    DIVISION_OUTER = 0
    OPTI_ALGORITHM = 1
    KWARGS_ALGO = 3

    def __init__(self, theGenerator=MyGenerator):
        super().__init__()

        self.maxTime = None  # set by set_maxtime
        self.theEvaluator = None  # set by set_evaluator
        self.theGenerator = theGenerator

        self.terminationConditions = SeveralTerminationCondition()
        self.kwargs_opti_algorithm = dict()  # Additional kwargs opti_algorithm

        self.add_option(self.OPTI_ALGORITHM, Option_str("Optimization algorithm", 'NSGAII', choices=["NSGAII", "NSGAIII", "OMOPSO", "SPEA2", "SMPSO", "GA", "GDE3"]))
        self.add_option(self.KWARGS_ALGO, Option_dict("Keywords arguments to send to the optimization algorithm", {}))

        self.array_evaluator = False
        self.algorithm = None

    def initialize(self, initialVectorGuess, listOfOptimizationVariables):
        """This function is called just before running optimization algorithm."""

        numberOfObjectives = len(self.theEvaluator.settings.get_objectives())
        numberOfConstraints = len(self.theEvaluator.settings.get_constraints())

        theProblem = MyProblem(listOfOptimizationVariables, numberOfObjectives, numberOfConstraints)

        kwargs = {"generator": self.theGenerator(initialVectorGuess), "convergence": EvolutionaryConvergence(), "evaluator": PlatypusToOptimeed_Evaluator(self.theEvaluator)}

        # Update variator if different types to optimize
        base_type = theProblem.types[0].__class__
        if not all([isinstance(t, base_type) for t in theProblem.types]) and not self.get_option_value(self.OPTI_ALGORITHM) == 'GDE3':
            # Explicit mutation and cross-over variables (even if they are the default values)
            # In the future we might want to give access to these variables to the user directly
            mutation_prob = 1
            mutation_di = 20
            co_prob = 1
            co_di = 15
            kwargs.update({"variator": 
            CompoundOperator(SBX(probability=co_prob, distribution_index=co_di), 
            HUX(probability=co_prob), 
            PM(probability=mutation_prob, distribution_index=mutation_di), 
            BitFlip(probability=mutation_prob))})
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'GDE3':
            kwargs.update({"variator": DifferentialEvolution(crossover_rate=0.1, step_size=0.5)})

        kwargs.update(self.get_option_value(self.KWARGS_ALGO))

        # Set optimization algorithm
        divisions_outer = int(30 * numberOfObjectives)
        if self.get_option_value(self.OPTI_ALGORITHM) == 'SPEA2':
            algorithm = SPEA2(theProblem, **kwargs)
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'SMPSO':
            algorithm = SMPSO(theProblem, **kwargs)
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'OMOPSO':
            algorithm = OMOPSO(theProblem, epsilons=[0.05], **kwargs)
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'NSGAII':
            algorithm = NSGAII(theProblem, **kwargs)  # self.get_option_value(self.DIVISION_OUTER))
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'NSGAIII':
            algorithm = NSGAIII(theProblem, divisions_outer, **kwargs)  # self.get_option_value(self.DIVISION_OUTER))
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'GA':
            algorithm = GeneticAlgorithm(theProblem, **kwargs)
        elif self.get_option_value(self.OPTI_ALGORITHM) == 'GDE3':
            algorithm = GDE3(theProblem, **kwargs)
        else:
            raise NotImplementedError("This algorithm has not been yet implemented {}".format(self.get_option_value(self.OPTI_ALGORITHM)))
        self.algorithm = algorithm

    def compute(self):
        self.terminationConditions.add(MaxTimeTerminationCondition(self.maxTime))
        self.algorithm.run(self.terminationConditions)

        self.algorithm.evaluator.close()

        def decode_solution_platypus(var_solutions, var_optimisations):
            my_solutions = [None] * len(var_solutions)
            for k, type_var in enumerate(var_optimisations):
                my_solutions[k] = type_var.decode(var_solutions[k])
            return my_solutions

        return [decode_solution_platypus(solution.variables, self.algorithm.problem.types) for solution in unique(nondominated(self.algorithm.result)) if solution.feasible]

    def set_evaluator(self, theEvaluator):
        self.theEvaluator = theEvaluator

    def set_maxtime(self, maxTime):
        self.maxTime = maxTime

    def __str__(self):
        theStr = ''
        theStr += "Platypus multiobjective library\n"
        theStr += indentParagraph(super().__str__(), indent_level=1)
        return theStr

    def get_convergence(self):
        """This function is called just before compute. Because the convergence is contained in opti algorithm, it must be created now."""
        return self.algorithm.convergence

    def add_terminationCondition(self, theTerminationCondition):
        self.terminationConditions.add(theTerminationCondition)

    def reset(self):
        terminationConditions = self.terminationConditions
        kwargs_opti_algorithm = self.kwargs_opti_algorithm
        super().reset()
        self.terminationConditions = terminationConditions
        self.kwargs_opti_algorithm = kwargs_opti_algorithm
