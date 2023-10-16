from optimeed.core import printIfShown, SHOW_WARNING, SHOW_DEBUG
import traceback
import copy
import math
import time
import os


def get_evaluate_args(opti_settings):
    arguments = dict()
    arguments['objectives'] = opti_settings.get_objectives()
    arguments['constraints'] = opti_settings.get_constraints()
    arguments['M2P'] = opti_settings.get_M2P()
    arguments['optivariables'] = opti_settings.get_optivariables()
    arguments['device'] = opti_settings.get_device()
    arguments['charac'] = opti_settings.get_charac()
    return arguments


def _evaluate(x, arguments):
    theObjectives = arguments['objectives']
    theConstraints = arguments['constraints']
    theMathsToPhysics = arguments['M2P']
    theOptimizationVariables = arguments['optivariables']
    copyDevice = copy.copy(arguments['device'])
    theCharacterization = arguments['charac']

    theMathsToPhysics.fromMathsToPhys(x, copyDevice, theOptimizationVariables)

    characterization_failed = False
    # noinspection PyBroadException
    try:
        theCharacterization.compute(copyDevice)
    except Exception:
        characterization_failed = True
        printIfShown("An error in characterization. Set objectives to inf. Error :" + traceback.format_exc(), SHOW_WARNING)

    nbr_of_objectives = len(theObjectives)
    objective_values = [float('inf')] * nbr_of_objectives

    nbr_of_constraints = len(theConstraints)
    constraint_values = [float('inf')] * nbr_of_constraints

    if not characterization_failed:
        for i in range(nbr_of_objectives):
            # noinspection PyBroadException
            try:
                objective_values[i] = theObjectives[i].compute(copyDevice)
                if math.isnan(objective_values[i]):
                    objective_values[i] = float('inf')
            except Exception:
                objective_values[i] = float('inf')
                printIfShown("An error in objectives. inf value has been set to continue execution. Error:" + traceback.format_exc(), SHOW_DEBUG)

        for i in range(nbr_of_constraints):
            # noinspection PyBroadException
            try:
                constraint_values[i] = theConstraints[i].compute(copyDevice)
            except Exception:
                constraint_values[i] = float('inf')
                printIfShown("An error in constraints. NaN value has been set to continue execution. Error:" + traceback.format_exc(), SHOW_DEBUG)

    returned_values = dict()
    returned_values["params"] = x
    returned_values["device"] = copyDevice
    returned_values["time"] = time.time()
    returned_values["objectives"] = objective_values
    returned_values["constraints"] = constraint_values
    return returned_values
