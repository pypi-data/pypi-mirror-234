from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSignal


class widget_doubleSlider(QSlider):
    doubleValueChanged = pyqtSignal(float)

    def __init__(self, decimals=3, *args, **kwargs):
        """
        Like a QSlider but accepts float numbers
        :param decimals: number of decimals to account for
        :param args: args to pass to QSlider
        :param kwargs: kwargs to pass to QSlider
        """
        super().__init__(*args, **kwargs)
        self._multi = 10 ** decimals

        self.valueChanged.connect(self.emitDoubleValueChanged)

    def emitDoubleValueChanged(self):
        value = float(super().value())/self._multi
        self.doubleValueChanged.emit(value)

    def value(self):
        return float(super().value()) / self._multi

    def setMinimum(self, value):
        return super().setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super().setMaximum(value * self._multi)

    def setSingleStep(self, value):
        return super().setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super().singleStep()) / self._multi

    def setValue(self, value):
        super().setValue(int(value * self._multi))