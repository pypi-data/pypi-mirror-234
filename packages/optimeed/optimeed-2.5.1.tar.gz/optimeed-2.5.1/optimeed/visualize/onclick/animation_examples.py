from optimeed.visualize.widgets import Widget_text_scrollable, Widget_lineDrawer
from .animationGUI import AnimationGUI


class Animate_openGL(AnimationGUI):
    """Implements :class:`~DataAnimationVisuals` to show opengl drawing"""
    def __init__(self, theOpenGLWidget, theId=0, window_title='Animation'):
        super().__init__(theId, window_title)
        self.theOpenGLWidget = theOpenGLWidget
        self.horizontal_layout_visu.addWidget(self.theOpenGLWidget)

    def update_widget_w_animation(self, key, index, the_data_animation):
        self.theOpenGLWidget.set_deviceToDraw(the_data_animation.get_element_animations(0, index))

    def export_widget(self, painter):
        pass

    def delete_key_widgets(self, key):
        pass


class Animate_openGL_and_text(Animate_openGL):
    """Implements :class:`~DataAnimationVisuals` to show opengl drawing and text"""
    def __init__(self, *args, is_light=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.textWidget = Widget_text_scrollable('', is_light=is_light, convertToHtml=False)
        self.horizontal_layout_visu.addWidget(self.textWidget)

    def update_widget_w_animation(self, key, index, the_data_animation):
        super().update_widget_w_animation(key, index, the_data_animation)
        self.textWidget.set_text(the_data_animation.get_element_animations(1, index), convertToHtml=True)

    def get_interesting_elements(self, devices_list):
        all_listOfText = [str(device) for device in devices_list]
        return [devices_list, all_listOfText]


class Animate_lines(AnimationGUI):
    """Implements :class:`~DataAnimationVisuals` to show drawing made out of lines (:class:`~optimeed.visualize.gui.widgets.widget_line_drawer`)"""
    def __init__(self, get_lines_method, is_light=True, theId=0, window_title='Animation'):
        """

        :param get_lines_method: Method that takes Device as argument and returns list of lines
        :param is_light:
        :param theId:
        :param window_title:
        """
        super().__init__(theId, window_title)
        self.qtLinesDrawer = Widget_lineDrawer(is_light=is_light)
        self.horizontal_layout_visu.addWidget(self.qtLinesDrawer)
        self.get_lines_method = get_lines_method

    def export_widget(self, painter):
        self.qtLinesDrawer.paintEvent(event=None, painter=painter)

    def delete_key_widgets(self, key):
        self.qtLinesDrawer.delete_lines(key)

    def update_widget_w_animation(self, key, index, the_data_animation):
        self.qtLinesDrawer.set_lines(the_data_animation.get_element_animations(0, index), key_id=key, pen=the_data_animation.get_base_pen())

    def get_interesting_elements(self, devices_list):
        all_listsOfLines = [self.get_lines_method(device) for device in devices_list]
        all_listOfText = [str(device) for device in devices_list]
        return [all_listsOfLines, all_listOfText]


class Animate_lines_and_text(Animate_lines):
    """Same as :class:`~DataAnimationLines` but also with text"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textWidget = Widget_text_scrollable('', is_light=kwargs.get("is_light", True), convertToHtml=False)
        self.horizontal_layout_visu.addWidget(self.textWidget)

    def update_widget_w_animation(self, key, index, the_data_animation):
        self.qtLinesDrawer.set_lines(the_data_animation.get_element_animations(0, index), key_id=key, pen=the_data_animation.get_base_pen())
        self.textWidget.set_text(the_data_animation.get_element_animations(1, index), convertToHtml=True)

