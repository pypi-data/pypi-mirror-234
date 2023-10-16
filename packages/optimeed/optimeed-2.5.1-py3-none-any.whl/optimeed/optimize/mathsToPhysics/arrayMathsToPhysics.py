from .interfaceMathsToPhysics import InterfaceMathsToPhysics
import numpy as np
from optimeed.core import rsetattr


class ArrayMathsToPhysics(InterfaceMathsToPhysics):
    """Evaluate array M2P. Only use it if specifically needed"""
    def fromMathsToPhys(self, list_of_xvector, theDevice, theOptimizationVariables):
        for i in range(len(theOptimizationVariables)):
            rsetattr(theDevice, theOptimizationVariables[i].get_attribute_name(), np.array([xvector[i] for xvector in list_of_xvector]))

    def fromPhysToMaths(self, theDevice, theOptimizationVariables):
        x01 = [None]*len(theOptimizationVariables)
        for i, optimizationVariable in enumerate(theOptimizationVariables):
            x01[i] = optimizationVariable.get_PhysToMaths(theDevice)
        return np.array(x01)

    def __str__(self):
        return "Dummy maths to physics"
