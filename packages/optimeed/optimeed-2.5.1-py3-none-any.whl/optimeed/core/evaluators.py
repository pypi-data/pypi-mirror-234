"""This file contains higher interface evaluators that allow parallel runs and callbacks in the main thread.
They are used in two places: Sensitivity analyses and Optimization
Usage:
-> initialize with "settings" as argument
-> use set_evaluation_function(function, arguments_function)
-> use add_callback(callback_function) for a callback
-> use start before running the algorithm
-> use close to properly close the processes (if any)
When using evaluator.evaluate(job), the evaluator calls function(job, arguments_function(settings))
We call evaluator.callbacks(result)
and then return the result
The method evaluator.evaluate_all(jobs), then parallel run might be working (depending on the subclass of Evaluator).
"""

from optimeed.core.tools import printIfShown
from optimeed.core.commonImport import SHOW_INFO
from multiprocessing import Pool, cpu_count, Process, Queue
from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    def __init__(self, settings):
        self.settings = settings
        self.callbacks = set()
        self._evaluate = None
        self._get_evaluate_args = None

    def set_evaluation_function(self, evaluate_function, get_evaluate_args):
        self._evaluate = evaluate_function
        self._get_evaluate_args = get_evaluate_args

    def start(self):
        """Function that is called once just before starting the optimization"""
        pass

    def close(self):
        """Function that is called once after performing the optimization"""
        pass

    def do_callbacks(self, result_evaluation):
        """Perform the callbacks. Check `meth`:_evaluate for args"""
        for callback in self.callbacks:
            callback(result_evaluation)

    def add_callback(self, callback):
        """Add a callback method, to call everytime a point is evaluated"""
        self.callbacks.add(callback)

    @abstractmethod
    def evaluate(self, x):
        """Perform a single evaluation. Should slowly become deprecated (evaluate_all is more efficient)
        :param x: list of values [val1, val2, ..., valN] that are associated to the optimization parameters [1, 2, ..., N]
        :return output: output of :meth:`_evaluate`
        """
        pass

    @abstractmethod
    def evaluate_all(self, list_of_x):
        """Same as :meth:`AbstractEvaluator.evaluate`, but for a list of inputs (allow parallel run)
        :param list_of_x: list of args of :meth:`_evaluate`
        :return list of outputs of :meth:`_evaluate`
        """
        pass


class Evaluator(AbstractEvaluator):
    """Default evaluator that does not use parallel evaluations. => No risk of collision between concurrent threads. """
    def evaluate(self, x):
        results = self._evaluate(x, self._get_evaluate_args(self.settings))
        self.do_callbacks(results)
        return results

    def evaluate_all(self, list_of_x):
        return [self.evaluate(x) for x in list_of_x]


class MultiprocessEvaluator(Evaluator):
    """Allows multiprocess run. The arguments of _evaluate are NOT process safe: i.e. a new copy of
    characterization, objectives, constraints, device are copy at each call of :meth:`MultiprocessEvaluator.evaluate_all`
    In most of the cases it should be adequate, but this can be limiting if initialization of these classes is long.
    """
    def __init__(self, settings, number_of_cores=1):
        super().__init__(settings)
        self.pool = Pool(min(cpu_count(), number_of_cores))

    def evaluate_all(self, list_of_x):
        # There is a subtlety here: using multiprocess, both the args and the functions must be pickable
        # The function is pickled because on separate files => ok
        # Most of the optisettings are pickable, except the optialgorithm, that also references this class (MultiprocessEvaluator) => cannot be pickled
        # We, however, do not use it for the evaluation => use get_evaluate_args for those that need pickling.
        outputs = [self.pool.apply_async(self._evaluate, args=(x, self._get_evaluate_args(self.settings),), callback=self.do_callbacks) for x in list_of_x]
        return [output.get() for output in outputs]  # Same order as list_of_x => ok

    def close(self):
        printIfShown("Closing Pool", SHOW_INFO)
        self.pool.close()
        printIfShown("Waiting for all processes to complete", SHOW_INFO)
        self.pool.join()
        printIfShown("Pool closed", SHOW_INFO)


def evaluate_with_queue(evaluate_function, evaluate_args, queue_evaluate, queue_results):
    while True:
        index, x = queue_evaluate.get()
        if x == 'exit':  # Exit signal from queue
            break
        results_evaluation = evaluate_function(x, evaluate_args)
        queue_results.put((index, results_evaluation))


class PermanentMultiprocessEvaluator(AbstractEvaluator):
    """Allows multiprocess run. Conversely to :class:`MultiprocessEvaluator`, it uses a system of queue to send and gather results.
    The guarantees are the following: the arguments resulting of :meth:`get_evaluate_args` will be forked only once at the creation of the processes.
    Each process will be kept alive afterwards, and can reuse the same arguments
    => Useful when initializing the models generates a lot of overhead.
    """
    def __init__(self, settings, number_of_cores=1):
        super().__init__(settings)
        self.all_processes = list()
        self.queue_evaluate = Queue()
        self.queue_results = Queue()
        self.number_of_cores = min(cpu_count(), number_of_cores)

    def start(self):
        evaluate_args = self._get_evaluate_args(self.settings)
        for i in range(self.number_of_cores):
            new_p = Process(target=evaluate_with_queue, args=(self._evaluate, evaluate_args, self.queue_evaluate, self.queue_results,), name='Worker {}'.format(i))
            new_p.start()
            self.all_processes.append(new_p)  # Keep them references

    def evaluate(self, x):
        self.queue_evaluate.put((0, x))
        return self.queue_results.get()

    def evaluate_all(self, list_of_x):
        for index, x in enumerate(list_of_x):
            self.queue_evaluate.put((index, x))

        num_to_complete = len(list_of_x)
        outputs = [None]*num_to_complete
        num_completed = 0
        while num_completed < num_to_complete:
            index, results = self.queue_results.get()
            self.do_callbacks(results)
            outputs[index] = results
            num_completed += 1
        return outputs

    def close(self):
        printIfShown("Setting signals to stop processes", SHOW_INFO)
        for _ in range(len(self.all_processes)):
            self.queue_evaluate.put((0, 'exit'))

        printIfShown("Waiting for all processes to complete", SHOW_INFO)
        for p in self.all_processes:
            p.join()

        printIfShown("All processed have been successfully stopped", SHOW_INFO)
