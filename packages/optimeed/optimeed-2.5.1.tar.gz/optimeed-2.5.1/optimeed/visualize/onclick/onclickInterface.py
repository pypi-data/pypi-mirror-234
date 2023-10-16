from abc import ABCMeta, abstractmethod

class OnclickInterface(metaclass=ABCMeta):
    """Interface class for the action to perform when a point is clicked"""

    @abstractmethod
    def graph_clicked(self, theGraphsVisual, index_graph, index_trace, indices_points):
        """
        Action to perform when a graph is clicked

        :param theGraphsVisual: class widget_graphs_visual that has called the method
        :param index_graph: Index of the graph that has been clicked
        :param index_trace: Index of the trace that has been clicked
        :param indices_points: graph Indices of the points that have been clicked
        :return:
        """
        pass

    @abstractmethod
    def get_name(self):
        pass