from FTV.FrameWork.Features import NIFeature
from FTV.FrameWork.Apps import NIApp
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DyInt


class Feature1(NIFeature):
    pass


class Feature2(NIFeature):
    pass


class VM(VariableManager):
    def setupVariables(self):
        self.c = DyInt(0)


class FM(FeatureManager):
    def setupFeatures(self):
        self.addFeature(Feature1)
        self.addFeature(Feature2)


class App(NIApp):
    def setupManagers(self):
        self.setVariableManager(VM)
        self.setFeatureManager(FM)

    def setupTriggers(self):
        self.addTrigger(self.vm.START).setAction(self.print_A)
        self.addTrigger(self.vm.c).setAction(self.print_c)

    @DyMethod()
    def print_A(self):
        Log.p("A")
        self.vm.c += 1

    @DyMethod()
    def print_c(self):
        Log.p("self.c: " + str(self.vm.c))
