import os
import traceback
from PyQt5 import QtCore, QtWidgets

from optimeed.core.inkscape_manager import inkscape_svg_to_pdf, inkscape_svg_to_png
from optimeed.core.tools import printIfShown, SHOW_WARNING
from optimeed.core.tikzTranslator import export_to_tikz_groupGraphs

from .pyqtgraph import setConfigOption, setConfigOptions
from .pyqtgraph.exporters.SVGExporter import SVGExporter
from .pyqtgraphRedefine import myGraphicsLayoutWidget

from .traceVisual import TraceVisual
from .graphVisual import GraphVisual

from optimeed.visualize.widgets import Widget_menuButton


class Widget_graphsVisualLite(QtWidgets.QWidget):
    """Widget element to draw a graph. The traces and graphs to draw are defined in :class:`~optimeed.visualize.graphs.Graphs.Graphs` taken as argument.
     This widget is linked to the excellent third-party library pyqtgraph, under MIT license"""
    signal_must_update = QtCore.pyqtSignal()  # Use this signal to refresh the graphs (signal_must_update.emit())
    signal_graph_changed = QtCore.pyqtSignal()  # This signal is sent when the graph layout is changed (number of traces/graphs)

    def __init__(self, theGraphs, **kwargs):
        """

        :param theGraphs: :class:`~optimeed.visualize.graphs.Graphs.Graphs`.
        :param is_light: Light theme option (bool)
        :param refresh_time: Refresh time (in seconds). If < 0: never automatically refreshed.
        :param highlight_last: Option to automatically highlight last point added in data.
        :param linkX: Link the x-axis of the graphs together (bool)
        :param actionOnClick: Action to perform when a point is clicked. Calls the method :meth:`~on_graph_click_interface.graph_clicked`.
        """
        self.is_light = kwargs.get('is_light', False)
        self.refresh_time = kwargs.get('refresh_time', 0.1) * 1000
        self.highlight_last = kwargs.get('highlight_last', False)
        self.linkX = kwargs.get('linkX', False)
        self.theActionOnClick = kwargs.get('actionOnClick', None)

        super().__init__()

        # Configure pyqtgraphs
        if self.is_light:  # Template "Light"
            background_color = 'w'
            foreground_color = (50, 50, 50)
            self.label_color = '#000'
        else:
            background_color = (30, 30, 30)
            foreground_color = (200, 200, 200)
            self.label_color = '#FFF'

        setConfigOption("antialias", True)
        setConfigOption('background', background_color)  # Color of background
        setConfigOption('foreground', foreground_color)  # Color of ticks
        setConfigOptions(useOpenGL=True)  # Otherwise performance issue on line thickness
        # pg.setConfigOption("crashWarning", True)

        # Initializes upper widget and core variables

        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        self.canvasWidget = myGraphicsLayoutWidget()
        main_vertical_layout.addWidget(self.canvasWidget)


        # self.theTraces = dict()
        # self.theWGPlots = dict()
        self.theGraphs = dict()
        self.theGraphsVisual = dict()

        # Create graphs
        self.theGraphs = theGraphs
        theGraphs.add_update_method(lambda: self.signal_must_update.emit())

        if self.linkX:
            self.link_axes()

        self.update_graphs(singleUpdate=False)
        self.canvasWidget.showMaximized()

        # connect signals
        self.signal_must_update.connect(self.update_graphs)

    def set_graph_disposition(self, indexGraph, row=1, col=1, rowspan=1, colspan=1):
        """
        Change the graphs disposition.

        :param indexGraph: index of the graph to change
        :param row: row where to place the graph
        :param col: column where to place the graph
        :param rowspan: number of rows across which the graph spans
        :param colspan: number of columns across which the graph spans
        :return:
        """
        item = self.get_graph(indexGraph).theWGPlot
        self.canvasWidget.ci.set_graph_disposition(item, row, col, rowspan, colspan)

    def __create_graph(self, idGraph):
        self.theGraphsVisual[idGraph] = GraphVisual(self)

    def __check_graphs(self):
        graph_changed = False
        """If the graphs have been modified, update them."""
        graphs2D = self.theGraphs.get_all_graphs_ids()
        # # Check the graphs

        # Create non existing graphs
        for idGraph in graphs2D:
            if idGraph not in self.theGraphsVisual:
                graph_changed = True
                self.__create_graph(idGraph)  # Create a graph
        # Remove graphs that disappeared
        indexToRemove = []
        for idGraph in self.theGraphsVisual:
            if idGraph not in graphs2D:
                graph_changed = True
                indexToRemove.append(idGraph)
        for idGraph in indexToRemove:
            self.delete_graph(idGraph)

        # # Check the traces
        for idGraph in self.theGraphsVisual:
            graphVisual = self.theGraphsVisual[idGraph]
            traces = self.theGraphs.get_graph(idGraph).get_all_traces()
            tracesVisual = graphVisual.get_all_traces()
            # Create non existing traces
            for idTrace, trace in traces.items():
                if idTrace not in tracesVisual:
                    graph_changed = True
                    graphVisual.add_data(idTrace, trace)  # Create the traces

            # Remove traces that  disappeared
            indexToRemove = []
            for idTrace in tracesVisual:
                if idTrace not in traces:
                    graph_changed = True
                    indexToRemove.append(idTrace)

            for idTrace in indexToRemove:
                graphVisual.delete_trace(idTrace)

            # Set color
            graphVisual.apply_palette()

            graphVisual.set_legend()

            if graph_changed:
                self.signal_graph_changed.emit()

    def on_click(self, plotDataItem, clicked_points):  # Clicked_points = list of spotItem
        indices_points = [0]*len(clicked_points)
        index_graph = 0
        index_trace = 0

        # Get index of point

        all_points = plotDataItem.scatter.points().tolist()
        for i, point in enumerate(clicked_points):
            indices_points[i] = all_points.index(point)

        # get index of graph
        for idGraph, graphVisual in self.theGraphsVisual.items():
            for idTrace, traceVisual in graphVisual.get_all_traces().items():
                if traceVisual.thePlotItem == plotDataItem:
                    index_graph = idGraph
                    index_trace = idTrace

        if self.theActionOnClick is not None:
            # noinspection PyBroadException
            try:
                self.theActionOnClick.graph_clicked(self, index_graph, index_trace, indices_points)
            except Exception:
                printIfShown("Following error occurred in action on click :" + traceback.format_exc(), SHOW_WARNING)

    def update_graphs(self, singleUpdate=True):
        """
        This method is used to update the graph. This is fast but NOT safe (especially when working with threads).
        To limit the risks, please use self.signal_must_update.emit() instead.

        :param singleUpdate: if set to False, the graph will periodically refres each self.refreshtime
        """
        self.__check_graphs()
        # self.fast_update()
        for graph in self.theGraphsVisual.values():
            graph.update()
        if self.refresh_time > 0 and not singleUpdate:
            QtCore.QTimer().singleShot(self.refresh_time, lambda: self.update_graphs(False))

    def fast_update(self):
        """Use this method to update the graph in a fast way. NOT THREAD SAFE."""
        for graph in self.theGraphsVisual.values():
            graph.fast_update()

    def select_folder_and_export(self):
        dlg = QtWidgets.QFileDialog.getSaveFileName()[0]
        self.exportGraphs(dlg)

    def exportGraphs(self, filename):
        """Export the graphs"""
        if filename:
            root, ext = os.path.splitext(filename)
            ext_svg = '.svg'
            ext_png = '.png'
            ext_pdf = '.pdf'
            ext_txt = '.txt'
            ext_tikz = '.tikz'

            if ext == ext_txt or not ext:
                self.export_txt(root + ext_txt)

            if ext == ext_svg or not ext or ext in [ext_png, ext_pdf]:
                self.export_svg(root + ext_svg)

            if ext == ext_png or not ext:
                inkscape_svg_to_png(root + ext_svg, root + ext_png)

            if ext == ext_pdf or not ext:
                inkscape_svg_to_pdf(root + ext_svg, root + ext_pdf)

            if ext == ext_tikz or not ext:
                self.export_tikz(root)

    def export_txt(self, filename_txt):
        theStr = self.theGraphs.export_str()
        with open(filename_txt, 'w') as f:
            f.write(theStr)

    def export_svg(self, filename):
        my_exporter = SVGExporter(self.canvasWidget.sceneObj)
        my_exporter.params.param('scaling stroke').setValue(True)
        my_exporter.export(filename)

    def export_tikz(self, foldername_tikz):
        # Additional parameters for tikz: log axes
        def additionalAxisOptions(graphId):
            theStr = ''
            gridstyle = "grid style={solid},"
            if self.get_graph(graphId).theWGPlot.ctrl.logXCheck.isChecked():
                theStr += "xmode=log,xtickten={0,...,10}," + gridstyle
            if self.get_graph(graphId).theWGPlot.ctrl.logYCheck.isChecked():
                theStr += "ymode=log,ytickten={0,...,10}," + gridstyle
            # axisX = self.get_graph(graphId).get_axis("bottom")
            # axisY = self.get_graph(graphId).get_axis("left")
            # xrange = axisX.range
            # yrange = axisY.range
            # theStr += "xmin={}, xmax={}\n, ymin={}, ymax={}\n".format(*xrange, *yrange)
            return theStr

        # def additionalTraceOptions(graphId, traceId):
        #     theStr = ''
        #     # theColor = self.get_graph(graphId).get_trace(traceId).get_color()
        #     # if self.theGraphs.get_graph(graphId).get_trace(traceId).get_color() is None:
        #     #     theStr += "color={{rgb:red,{};green,{};blue,{}}},\n".format(*convert_color(theColor))
        #     return theStr
        export_to_tikz_groupGraphs(self.theGraphs, foldername_tikz, additionalAxisOptions=additionalAxisOptions)

    def link_axes(self):
        keys = list(self.theGraphsVisual.keys())
        for key in keys:
            self.theGraphsVisual[key].linkXToGraph(self.theGraphsVisual[keys[0]])

    def get_graph(self, idGraph) -> GraphVisual:
        """Get corresponding :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.GraphVisual.GraphVisual` of the graph idGraph"""
        return self.theGraphsVisual[idGraph]

    def get_trace(self, idGraph, idTrace) -> TraceVisual:
        """Get corresponding Tracevisual"""
        return self.get_graph(idGraph).get_trace(idTrace)

    def keyPressEvent(self, event):
        """
        What happens if a key is pressed.
        R: reset the axes to their default value
        """
        if event.key() == QtCore.Qt.Key_R:
            for idGraphVisual in self.get_all_graphsVisual():
                self.get_graph(idGraphVisual).theWGPlot.autoRange()
                # graphVisual.set_lims(self.theTraces[idGraph][0])

    def delete_graph(self, idGraph):
        """Delete the graph idGraph"""
        try:
            self.theGraphsVisual[idGraph].delete()
            self.theGraphsVisual.pop(idGraph)
        except KeyError:
            printIfShown("Graph already deleted", SHOW_WARNING)

    def delete(self):
        graphs_ids = list(self.get_all_graphsVisual().keys())
        for graphID in graphs_ids:
            self.delete_graph(graphID)
        self.deleteLater()

    def get_all_graphsVisual(self):
        """Return a dictionary {idGraph: :class:`~optimeed.visualize.gui.widgets.graphsVisualWidget.GraphVisual.GraphVisual`}."""
        return self.theGraphsVisual

    def get_layout_buttons(self):
        """Get the QGraphicsLayout where it's possible to add buttons, etc."""
        return self.horizontalLayoutGUI

    def set_actionOnClick(self, theActionOnClick):
        """Action to perform when the graph is clicked

        :param theActionOnClick: :class:`on_graph_click_interface`
        :return:
        """
        self.theActionOnClick = theActionOnClick

    def set_title(self, idGraph, titleName, **kwargs):
        """Set title of the graph

        :param idGraph: id of the graph
        :param titleName: title to set
        """
        self.get_graph(idGraph).set_title(titleName, **kwargs)


class Widget_graphsVisual(Widget_graphsVisualLite):
    """Create a gui for pyqtgraph with trace selection options, export and action on clic choices"""
    def __init__(self, *args, **kwargs):
        """See Widget_graphsVisualLite params. Extra:

        :param actionsOnClick: list of  :class:`~optimeed.visualize.onclick.onclickInterface.OnclickInterface`
        """
        super().__init__(*args, **kwargs)


        # # Add last buttons
        # Export button
        horizontalLayout = QtWidgets.QHBoxLayout()

        # self.centralLayout
        self.layout().addLayout(horizontalLayout)
        # main_vertical_layout.addLayout(horizontalLayoutGUI)

        # self.theGraphsVisual = graphsVisual
        self.actionsOnClick = kwargs.pop('actionsOnClick', list())

        # Define buttons
        # horizontalLayout = self.theGraphsVisual.get_layout_buttons()

        button = QtWidgets.QPushButton('Export Graphs')
        button.clicked.connect(self.select_folder_and_export)
        horizontalLayout.addWidget(button)

        # Action button
        self.actionSelector = QtWidgets.QComboBox()
        self.actionSelector.currentIndexChanged.connect(lambda index: self.set_actionOnClick(self.actionsOnClick[index]))

        if self.actionsOnClick:
            self.set_actions_on_click(self.actionsOnClick)

        horizontalLayout.addWidget(self.actionSelector)

        # Link axes button
        button = QtWidgets.QPushButton('Link axes')
        button.clicked.connect(self.link_axes)
        horizontalLayout.addWidget(button)

        # Traces manager button
        button = QtWidgets.QPushButton('Manage traces')
        self.traceManager = Widget_menuButton(button)
        horizontalLayout.addWidget(button)
        self.signal_graph_changed.connect(lambda: self.refreshTraceList())
        self.refreshTraceList()

    def refreshTraceList(self):
        """Refresh all the traces"""
        self.traceManager.clear()
        graphsVisuals = self.get_all_graphsVisual()
        for graphId in self.get_all_graphsVisual():
            theGraph = graphsVisuals[graphId]
            all_traces = theGraph.get_all_traces()
            for trace in all_traces.values():
                theAction = self.traceManager.addAction("[{}] ".format(graphId) + trace.get_data().get_legend())
                theAction.setCheckable(True)
                theAction.setChecked(True)
                theAction.toggled.connect(trace.toggle)

    def set_actions_on_click(self, actions):
        self.actionsOnClick = actions
        for action in self.actionsOnClick:
            self.actionSelector.addItem(action.get_name())
        self.actionSelector.setCurrentIndex(0)
        self.set_actionOnClick(self.actionsOnClick[0])
