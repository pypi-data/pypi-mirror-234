import signal
import sys
from PyQt5 import QtWidgets

if QtWidgets.QApplication.instance() is None:
    app = QtWidgets.QApplication(sys.argv)  # must initialize only once


def start_qt_mainloop():
    """Starts qt mainloop, which is necessary for qt to handle events"""

    def handler_quit(sign_number, _):
        app.quit()
        sys.exit(sign_number)

    try:
        signal.signal(signal.SIGINT, handler_quit)
    except AttributeError:
        pass
    try:
        signal.signal(signal.SIGTSTP, handler_quit)
    except AttributeError:
        pass
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app.exec()


def stop_qt_mainloop():
    """Stops qt mainloop and resumes to program"""
    app.quit()


def process_qt_events():
    """Process current qt events"""
    app.processEvents()
