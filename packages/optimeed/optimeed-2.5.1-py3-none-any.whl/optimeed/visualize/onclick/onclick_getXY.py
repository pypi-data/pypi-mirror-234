from .onclickInterface import OnclickInterface
from PyQt5.QtWidgets import QApplication
from optimeed.core import printIfShown, SHOW_INFO


class Onclick_getXY(OnclickInterface):
    """On click: display X and Y coordinates of the points"""
    def __init__(self):
        pass

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        X, Y = theGraphVisual.theGraphs.get_graph(index_graph).get_trace(index_trace).get_plot_data()
        theStr = "\n"
        theStr += "X = {}\n".format(X)
        theStr += "Y = {}".format(Y)
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(theStr, mode=cb.Clipboard)
        printIfShown("{}\nCopied to clipboard!".format(theStr), SHOW_INFO)

    def get_name(self):
        return "Get XY data"
