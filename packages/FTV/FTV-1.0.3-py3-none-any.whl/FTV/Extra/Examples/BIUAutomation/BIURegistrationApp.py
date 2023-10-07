from FTV.Extra.Examples.BIUAutomation.Features.CourseRegistration import CourseRegistration
from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread, DyThreadList
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        self.onReadyToSearchCourse = DySwitch()
        self.onCourseDetected = DySwitch()
        self.onCourseAvailable = DySwitch()
        self.onReadyToRegisterCourse = DySwitch()
        self.onCourseRegistered = DySwitch()

    def setupTriggers(self):
        pass


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()
        self.Workers = DyThreadList()


class FM(FeatureManager):
    def setupFeatures(self):
        self.addFeature(CourseRegistration)
        pass


class BIURegistrationApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)
        self.setVariableManager(VM)

    def setupTriggers(self):
        pass
