from FTV.FrameWork.Features import UIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Managers.UIManager import UIManager


class VM(VariableManager):

    def setupVariables(self):
        pass

class UIM(UIManager):
    def setupUIVariables(self):
        pass

class UIFeature1(UIFeature):

    @classmethod
    def setupManagers(cls):
        cls.vm = VM()
        cls.uim = UIM()

    def setupSettings(self):
        pass

    def setupTriggers(self):
        pass
        # self.addTrigger(self.fm.features, "Triger.List.len.Changed", "self.showPercentage")

