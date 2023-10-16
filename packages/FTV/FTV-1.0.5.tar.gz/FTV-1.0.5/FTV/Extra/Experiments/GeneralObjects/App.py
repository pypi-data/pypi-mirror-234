import abc
import sys

from PyQt5.QtWidgets import QApplication

from FTV.Extra.Experiments import Feature


global __app


class App(Feature):
    def __init__(self):
        super().__init__()
        __app = QApplication(sys.argv)

        self.initContainers()
        self.initFeatures()
        self.start()
        sys.exit(__app.exec_())
        # __app.exec_()

    @abc.abstractmethod
    def initContainers(self):
        pass

    @abc.abstractmethod
    def initFeatures(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass
