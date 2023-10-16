from .onclickInterface import OnclickInterface


class Onclick_delete(OnclickInterface):
    """On Click: Delete the points from the graph"""

    def __init__(self, theDataLink):
        """

        :param theDataLink: :class:`~optimeed.visualize.high_level.LinkDataGraph.LinkDataGraph`
        """
        super().__init__()
        self.theDataLink = theDataLink

    def graph_clicked(self, _theGraphVisual, index_graph, index_trace, indices_points):
        self.theDataLink.delete_clicked_items(index_graph, index_trace, indices_points)

    def get_name(self):
        return "Delete points"

