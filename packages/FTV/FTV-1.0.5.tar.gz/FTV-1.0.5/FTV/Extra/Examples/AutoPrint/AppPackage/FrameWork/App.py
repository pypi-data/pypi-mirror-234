from AppPackage.FrameWork.Features.UIFeature1 import UIFeature1
from FTV.FrameWork.Apps import UIApp, NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.LogManager import LogManager
from FTV.Managers.UIManager import UIManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects import UIPlatforms


class FM(FeatureManager):
    pass

class EM(ExecutionManager):
    pass

class VM(VariableManager):
    pass

class LM(LogManager):
    pass

class UIM(UIManager):
    pass

class App(UIApp):

    @classmethod
    def setupManagers(cls):
        cls.fm = FM()
        cls.em = EM()
        cls.vm = VM()
        cls.lm = LM()
        cls.uim = UIM()

    def setupSettings(self):
        pass
    #     self.settings.setUIPlatform(UIPlatforms.PyQt5)

    def setupFeatures(self):
        self.addFeature(UIFeature1)


if __name__ == '__main__':
    App()
