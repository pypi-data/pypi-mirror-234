import math
import numpy as np
from SALib.analyze import sobol
from SALib.sample import saltelli
from optimeed.optimize import Real_OptimizationVariable
from .sensitivity_analysis import SensitivityAnalysis_LibInterface


def _get_sensitivity_problem(list_of_optimization_variables):
    """
    This is the first method to use. Convert a list of optimization variables to a SALib problem

    :param list_of_optimization_variables: List of optimization variables
    :return: SALib problem
    """
    num_vars = len(list_of_optimization_variables)
    names = list()
    bounds = list()

    for variable in list_of_optimization_variables:
        if isinstance(variable, Real_OptimizationVariable):
            names.append(variable.get_attribute_name())
            bounds.append([variable.get_min_value(), variable.get_max_value()])
        else:
            raise TypeError("Optimization variable must be of real type to perform this analysis")
    problem = {'num_vars': num_vars, 'names': names, 'bounds': bounds}
    return problem


class SensitivityAnalysis_SALib(SensitivityAnalysis_LibInterface):
    def __init__(self, theSensitivityParameters, theObjectives):
        super().__init__(theSensitivityParameters, theObjectives)
        self.Si = None

    @staticmethod
    def sample_sobol(theOptimizationVariables, N):
        return saltelli.sample(_get_sensitivity_problem(theOptimizationVariables), N)

    def get_sobol_S1(self):
        return self._get_Si()['S1']

    def get_sobol_S1conf(self):
        return self._get_Si()['S1_conf']

    def get_sobol_S2(self):
        matrix = self._get_Si()['S2']
        nb_params = len(self.get_SA_params().get_optivariables())
        for i in range(nb_params):
            for j in range(i, nb_params):
                matrix[j, i] = matrix[i, j]
        return matrix

    def get_sobol_ST(self):
        return self._get_Si()['ST']

    def get_sobol_STconf(self):
        return self._get_Si()['ST_conf']

    def _get_Si(self):
        if not self.performed:
            self._analyze()
        return self.Si

    def _analyze(self):
        problem_SALib = _get_sensitivity_problem(self.get_SA_params().get_optivariables())
        nb_params = len(self.get_SA_params().get_optivariables())
        max_N = math.floor(len(self.theObjectives) / (2 * nb_params + 2))
        Si = sobol.analyze(problem_SALib, np.array(self.theObjectives[0:max_N * (2 * nb_params + 2)]))
        self.Si = Si
        self.performed = True
