from optimeed.visualize.widgets import Widget_openGL, Widget_lineDrawer, Widget_image, Widget_text_scrollable
from optimeed.core import rgetattr, str_all_attr
from .onclick_representDevice import RepresentDeviceInterface

class Represent_lines(RepresentDeviceInterface):
    def __init__(self, attribute_lines):
        """Uses Widget_lineDrawer to display the lines contained in attribute "attribute_lines"

        :param attribute_lines: name of attributes where the lines are stored
        """
        self.attribute_lines = attribute_lines

    def get_widget(self, theNewDevice):
        widgetLineDrawer = Widget_lineDrawer()
        widgetLineDrawer.set_lines(rgetattr(theNewDevice, self.attribute_lines))
        return widgetLineDrawer


class Represent_txt_function(RepresentDeviceInterface):
    def __init__(self, is_light=True, convertToHtml=True):
        """Display some text from the device

        :param is_light: Use light background
        :param convertToHtml: Convert text to html (for color support)
        """
        self.is_light = is_light
        self.convertToHtml = convertToHtml

    def getTxt(self, theNewDevice):
        return "Ici va le texte pour l'objet --> " + str(theNewDevice)

    def get_widget(self, theNewDevice):
        return Widget_text_scrollable(self.getTxt(theNewDevice), is_light=self.is_light, convertToHtml=self.convertToHtml)


class Represent_brut_attributes(RepresentDeviceInterface):
    def __init__(self, is_light=True, convertToHtml=True, recursion_level=5):
        """Loop through the attributes and display them as plain text

        :param is_light: Use light background
        :param convertToHtml: Convert text to html (for color support)
        :param recursion_level: Level of nesting to display
        """
        self.is_light = is_light
        self.convertToHtml = convertToHtml
        self.recursion_level = recursion_level

    def get_widget(self, theNewDevice):
        return Widget_text_scrollable(str_all_attr(theNewDevice, self.recursion_level), is_light=self.is_light, convertToHtml=self.convertToHtml)


class Represent_opengl(RepresentDeviceInterface):
    def __init__(self, DeviceDrawer):
        """
        Use openGL to represent the device

        :param DeviceDrawer: OpenGL drawer, see
        """

        self.DeviceDrawer = DeviceDrawer

    def get_widget(self, theNewDevice):
        theOpenGLWidget = Widget_openGL()
        theOpenGLWidget.set_deviceDrawer(self.DeviceDrawer)
        theOpenGLWidget.set_deviceToDraw(theNewDevice)
        return theOpenGLWidget


class Represent_image(RepresentDeviceInterface):
    def __init__(self, get_base_64_from_device):
        """
        Display an image (png) representation of the motor

        :param get_base_64_from_device: method taking a device as input and returns a base64 string
        """
        self.get_base_64_from_device = get_base_64_from_device

    def get_widget(self, theNewDevice):
        return Widget_image(self.get_base_64_from_device(theNewDevice))

