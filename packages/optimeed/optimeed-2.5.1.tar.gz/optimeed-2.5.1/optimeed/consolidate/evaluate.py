from optimeed.core import printIfShown, SHOW_WARNING
import traceback
import copy


def get_evaluate_args(sensitivity_settings):
    arguments = dict()
    arguments['M2P'] = sensitivity_settings.get_M2P()
    arguments['optivariables'] = sensitivity_settings.get_optivariables()
    arguments['device'] = sensitivity_settings.get_device()
    arguments['charac'] = sensitivity_settings.get_charac()
    arguments['variables_to_test'] = sensitivity_settings.get_paramvalues()
    return arguments


def _evaluate(index, arguments):
    x = arguments['variables_to_test'][index]
    theMathsToPhys = arguments['M2P']
    list_of_optimization_variables = arguments['optivariables']
    copyDevice = copy.copy(arguments['device'])
    theCharacterization = arguments['charac']

    output = dict()
    output["device"] = copyDevice
    output["x"] = x
    output["index"] = index

    theMathsToPhys.fromMathsToPhys(x, copyDevice, list_of_optimization_variables)
    # noinspection PyBroadException
    try:
        theCharacterization.compute(copyDevice)
        output["success"] = True
    except Exception:
        printIfShown("An error in characterization. Bypassing it to continue execution. Error :" + traceback.format_exc(), SHOW_WARNING)
        output["success"] = False

    return output
