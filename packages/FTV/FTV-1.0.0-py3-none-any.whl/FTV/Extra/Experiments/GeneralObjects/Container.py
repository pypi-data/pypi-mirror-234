import abc
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLayout, QLabel


class Cell:
    @abc.abstractmethod
    def set_layout(self):
        pass

    @abc.abstractmethod
    def set_container(self):
        pass

class MyCell(Cell):
    def set_container(self):
        pass

    def set_layout(self):
        pass

class Container:
    layout: QLayout = None
    frames: dict = {}

    __window = None
    __app = None
    __container = None

    _is_show = False

    @classmethod
    def __init__(cls):
        # cls = Feature.ui_platform.Container
        cls.__setupVariables()
        cls.setupUI()
        cls.layout.setContentsMargins(0,0,0,0)
        cls.layout.setSpacing(2)
        cls.__window.setLayout(cls.layout)

    @classmethod
    def __setupVariables(cls):
        cls.__window = QWidget()

    @classmethod
    def _setID(cls, frame, frame_id=None):
        if frame_id is None:
            frame_id = len(cls.frames)

        cls.frames[frame_id] = frame

    @abc.abstractmethod
    def setupUI(self):
        pass

    @abc.abstractmethod
    def setItem(self, *args):
        pass

    @classmethod
    def show(cls):
        cls._is_show = True
        cls.__window.show()

    @classmethod
    def hide(cls):
        cls._is_show = False
        cls.__window.hide()

    @classmethod
    def showDemo(cls):
        cls.__app = QApplication(sys.argv)

        cls.__container = cls()

        # Layout manipulations
        frames_len = len(cls.__container.frames)
        for index in range(frames_len):
            frame: QWidget = list(cls.frames.values())[index]
            key = list(cls.frames)[index]

            label = QLabel(key)
            label.setFont(QFont("Arial", 14))
            label.setAlignment(QtCore.Qt.AlignCenter)
            frame.addWidget(label)
            frame.setStyleSheet("background-color:skyBlue;");


        cls.__container.show()
        sys.exit(cls.__app.exec_())


    @classmethod
    def setCell(cls, container, id):
        if cls.getCell(id).count() == 1:
            cls.getCell(id).removeWidget(cls.getCell(id).currentWidget())

        widget = QWidget()
        widget.setLayout(container.layout)
        cls.getCell(id).addWidget(widget)

    @classmethod
    def getCell(cls, id):
        return cls.frames[id]
