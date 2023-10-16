from FTV.Extra.Experiments import App
from FTV.Extra.Experiments import Dialog, Dialog2, Dialog3, Dialog4
from FTV.Extra.Experiments.Objects.Containers.MainWindow import MainWindow
from FTV.Extra.Experiments import FeatureDemo
from FTV.Objects.SystemObjects import UIPlatforms


class AppDemo(App):
    def start(self):
        # Dialog.show()
        # Dialog2.show()
        MainWindow.show()

    def initContainers(self):
        MainWindow()
        Dialog()
        Dialog2()
        Dialog3()
        Dialog4()

    def initFeatures(self):
        FeatureDemo()

    def setSettings(self):
        self.setUIPlatform(UIPlatforms.PyQt5)


if __name__ == '__main__':
    AppDemo()
