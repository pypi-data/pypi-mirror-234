import time

from FTV.Tools.Log import Log
from FTV.FrameWork.Apps import NIApp
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DyInt


class VM(VariableManager):
    def setupVariables(self):
        self.a = DyInt(1)

    def setupTriggers(self):
        pass

class Feature1(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    # @classmethod
    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(App.vm.START).setAction(self.loopA)
        self.addTrigger(self.vm.a).setCondition(DyInt.IsChanged).setAction(self.printWorks)\
            .setThread(App.em.Sub)

    @DyMethod()
    def loopA(self):
        while self.vm.a < 10:
            self.increaseA()
            time.sleep(0.5)

    @DyMethod()
    def increaseA(self):
        self.vm.a += 1

    @DyMethod()
    def printWorks(self):
        Log.p("FTV Works!!!")


class EM(ExecutionManager):
    def setupThreads(self):
        self.Sub = DyThread()


class App(NIApp):
    def setupFeatures(self):
        # pass
        self.addFeature(Feature1)

    def setupSettings(self):
        pass

    # @classmethod
    def setupManagers(self):
        self.setExecutionManager(EM)
        pass


if __name__ == '__main__':
    App()
