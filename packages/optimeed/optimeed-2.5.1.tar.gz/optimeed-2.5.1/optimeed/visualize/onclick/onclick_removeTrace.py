from .onclickInterface import OnclickInterface


class Onclick_removeTrace(OnclickInterface):

    def __init__(self, theDataLink):
        """

        :param theDataLink: :class:`~optimeed.core.linkDataGraph.LinkDataGraph`
        """
        self.theDataLink = theDataLink

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, _):
        self.theDataLink.remove_collection(index_graph, index_trace)

    def get_name(self):
        return "Remove trace"
