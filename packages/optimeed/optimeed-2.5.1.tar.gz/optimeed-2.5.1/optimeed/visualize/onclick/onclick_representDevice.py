from .onclickInterface import OnclickInterface
from optimeed.core import printIfShown, SHOW_WARNING
from optimeed.visualize.mainWindow import MainWindow
import traceback
from abc import ABCMeta, abstractmethod


class RepresentDeviceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_widget(self, theDevice):
        """Get Qt widget that represents the device

        :param theDevice: the Device to be represented
        :return: Qt widget
        """
        pass


class Onclick_representDevice(OnclickInterface):
    """On click: show informations about the points (loop through attributes)"""

    class DataInformationVisuals:
        def __init__(self):
            self.listOfVisuals = {}
            self.theTraces = {}
            self.indicesPoints = {}
            self.index = 0

        def delete_visual(self, theVisual):
            goodkey = 0
            for key in self.listOfVisuals:
                if self.listOfVisuals[key] == theVisual:
                    goodkey = key
            self.theTraces[goodkey].reset_brush(self.indicesPoints[goodkey])

        def add_visual(self, theVisual, theTrace, indexPoint):
            theTrace.set_brush(indexPoint, (250, 250, 0))

            index = self.get_new_index()
            self.listOfVisuals[index] = theVisual
            self.indicesPoints[index] = indexPoint
            self.theTraces[index] = theTrace

            theVisual.move(10, 0)
            theVisual.setWindowTitle("Visual information of point " + str(index))
            # Put all previously opened window on top
            for key in self.listOfVisuals:
                self.listOfVisuals[key].raise_()

        def get_new_index(self):
            self.index += 1
            return self.index

        def curr_index(self):
            return self.index

    def __init__(self, theLinkDataGraph, visuals):
        """

        :param theLinkDataGraph: :class:`~optimeed.core.linkDataGraph.LinkDataGraph`
        :param visuals: List of classes following class:`RepresentDeviceInterface`
        """
        self.theLinkDataGraph = theLinkDataGraph
        self.dataInformationVisuals = self.DataInformationVisuals()
        self.visuals = visuals

    def graph_clicked(self, theGraphVisual, index_graph, index_trace, indices_points):
        """Action to perform when a point in the graph has been clicked:
        Creates new window displaying the device and its informations
        """
        try:
            def actionOnWindowClosed(theVisual, _):
                """Action to perform when a window has been closed:
                Remove the window from the dataInformationVisuals
                """
                theVisual.close()
                self.dataInformationVisuals.delete_visual(theVisual)

            theTrace = theGraphVisual.get_graph(index_graph).get_trace(index_trace)
            for index_point in indices_points:
                theDevice = self.theLinkDataGraph.get_clicked_item(index_graph, index_trace, index_point)

                theWidgetList = list()
                for visual in self.visuals:
                    theWidgetList.append(visual.get_widget(theDevice))

                visual_temp = MainWindow(theWidgetList, actionOnWindowClosed=actionOnWindowClosed)
                self.dataInformationVisuals.add_visual(visual_temp, theTrace, index_point)
                visual_temp.run(False)
        except KeyboardInterrupt:
            raise
        except Exception:
            printIfShown("Following error occurred in visualisation :" + traceback.format_exc(), SHOW_WARNING)

    def get_name(self):
        return "Represent Device"
