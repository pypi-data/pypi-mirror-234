from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicObjects import DyFloat


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()
        self.Algorithms = DyThread()


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.Algorithms.Features import BackgroundTasks
        from FTV.Extra.Examples.Algorithms.Features import ProgressBar

        self.addFeature(ProgressBar)
        self.addFeature(BackgroundTasks)


class VM(VariableManager):
    def setupVariables(self):
        self.progress = DyFloat(0, builtin=True)

    def setupTriggers(self):
        pass


class CalculationApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setFeatureManager(FM)
        self.setVariableManager(VM)
        self.setExecutionManager(EM)
