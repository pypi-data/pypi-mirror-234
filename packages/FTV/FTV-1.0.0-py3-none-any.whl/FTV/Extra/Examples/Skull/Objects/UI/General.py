import sys

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox


# def catch_exceptions(t, val, tb):
#     QMessageBox.critical(None,
#                                    "An exception was raised",
#                                    "Exception type: {}".format(t))
#     old_hook(t, val, tb)
#
#
# old_hook = sys.excepthook
# sys.excepthook = catch_exceptions


class AppRunner(QApplication):
    def __init__(self):
        super(AppRunner, self).__init__(sys.argv)
        self.widget: Widget = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.widget is not None:
            self.widget.show()

        if exc_type:
            raise exc_value

        sys.exit(self.exec_())

    def setApp(self, widget):
        self.widget = widget
        if "app_style" in dir(widget):
            self.setStyle(widget.app_style)

        if "app_palette" in dir(widget):
            self.setPalette(widget.app_palette)


class Widget(QWidget):
    def setTextSize(self, size, weight=1):
        self.setFont(QFont("Arial", size, weight))


class Worker(QObject):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.target(*self.args, **self.kwargs)
