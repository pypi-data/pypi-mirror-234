import abc
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLayout, QWidget, QApplication, QLabel


class AbsUIPlatform:
    class Container(abc.ABC):
        _frames: dict = {}
        __container = None

        @classmethod
        def __init__(cls):
            cls.setupVariables()

        @classmethod
        @abc.abstractmethod
        def setLayout(cls, *args):
            pass

        @classmethod
        @abc.abstractmethod
        def hide(cls):
            pass

        @classmethod
        @abc.abstractmethod
        def show(cls):
            pass

        @classmethod
        @abc.abstractmethod
        def showDemo(cls):
            pass

        @classmethod
        @abc.abstractmethod
        def setCell(cls, container, id):
            pass

        @classmethod
        @abc.abstractmethod
        def setupVariables(cls):
            pass

        @classmethod
        def setID(cls, frame, frame_id=None):
            if frame_id is None:
                frame_id = len(cls._frames)

            cls._frames[frame_id] = frame

        @classmethod
        def getCell(cls, id):
            return cls._frames[id]

class PyQt5(AbsUIPlatform):
    class Container(AbsUIPlatform.Container):

        window = None
        app = None

        @classmethod
        def setLayout(cls, layout: QLayout):
            cls.window.setLayout(layout)

        @classmethod
        def hide(cls):
            cls.window.hide()

        @classmethod
        def show(cls):
            cls.window.show()

        @classmethod
        def showDemo(cls):
            cls.app = QApplication(sys.argv)

            cls.__container = cls()

            # Layout manipulations
            _frames_len = len(cls.__container._frames)
            for index in range(_frames_len):
                frame: QWidget = list(cls._frames.values())[index]
                key = list(cls._frames)[index]

                label = QLabel(key)
                label.setFont(QFont("Arial", 14))
                label.setAlignment(QtCore.Qt.AlignCenter)
                frame.addWidget(label)
                frame.setStyleSheet("background-color:skyBlue;");

            cls.__container.show()
            sys.exit(cls.app.exec_())

        @classmethod
        def setCell(cls, container, id):
            if cls.getCell(id).count() == 1:
                cls.getCell(id).removeWidget(cls.getCell(id).currentWidget())

            widget = QWidget()
            widget.setLayout(container.layout)
            cls.getCell(id).addWidget(widget)

        @classmethod
        def setupVariables(cls):
            cls.window = QWidget()
