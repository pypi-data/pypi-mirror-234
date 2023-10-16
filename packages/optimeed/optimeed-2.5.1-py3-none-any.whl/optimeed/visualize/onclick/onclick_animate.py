from .onclickInterface import OnclickInterface
from optimeed.core import printIfShown, SHOW_WARNING
import traceback


class Onclick_animate(OnclickInterface):
    """On click: add or remove an element to animate"""

    def __init__(self, theLinkDataGraph, theAnimation):
        """

        :param theLinkDataGraph: :class:`~optimeed.visualize.high_level.LinkDataGraph.LinkDataGraph`
        :param theAnimation: :class:`~DataAnimationVisuals`
        """
        self.theLinkDataGraph = theLinkDataGraph
        self.theAnimation = theAnimation

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        try:
            trace_id = int(index_graph) * 100 + int(index_trace)
            theTrace = theGraphVisual.get_graph(index_graph).get_trace(index_trace)

            # index_in_data = theTrace.get_data().get_dataIndex_from_graphIndex(index_point)

            permutation = theTrace.theData.get_permutations()
            indicesInGraph = list(range(len(permutation)))  # Orders them accordingly to plot (data -> plot)
            all_listsOfDevices = self.theLinkDataGraph.get_clicked_items(index_graph, index_trace, indicesInGraph)

            # If trace wasn't present in any window ...
            if not self.theAnimation.contains_trace(trace_id):
                self.theAnimation.add_trace(trace_id, all_listsOfDevices, theTrace)
            for index_point in indices_points:
                index_in_graph = index_point
                self.theAnimation.add_elementToTrace(trace_id, index_in_graph)

            self.theAnimation.run()
        except KeyboardInterrupt:
            raise
        except Exception:
            printIfShown("Following error occurred in visualisation :" + traceback.format_exc(), SHOW_WARNING)

    def get_name(self):
        return "Animation"
