from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicObjects import DyInt


class VM(VariableManager):
    def setupVariables(self):
        self.tenth_seconds = DyInt(0)
        self.seconds = DyInt(0)
        self.minutes = DyInt(0)
        self.hours = DyInt(0)

    def setupTriggers(self):
        pass


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.DyClockExample.Features.IntegratedClock import IntegratedClock
        from FTV.Extra.Examples.DyClockExample.Features.VisualClock import VisualClock

        self.addFeature(IntegratedClock)
        self.addFeature(VisualClock)


class ClockApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)
        self.setVariableManager(VM)
