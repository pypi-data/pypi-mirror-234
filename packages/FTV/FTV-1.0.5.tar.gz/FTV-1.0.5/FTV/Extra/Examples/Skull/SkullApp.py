
from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicObjects import DySwitch, DyInt, DyStr


class VM(VariableManager):
    def setupVariables(self):
        self.onRecordStarted = DySwitch()
        self.onExamCancelRequested = DySwitch()
        self.onExamCanceled = DySwitch()

        self.onRecordFailure = DySwitch()
        self.onRecordCompleted = DySwitch()
        self.onRecordProgressUpdate = DySwitch()
        self.onSendExamStarted = DySwitch()
        self.onSendExamFailure = DySwitch()
        self.onSendExamCompleted = DySwitch()
        self.onSendExamProgressUpdate = DySwitch()

        self.onWindowOpened = DySwitch()
        self.onWindowClosed = DySwitch()

        self.recordProgress = DyInt(0)
        self.uploadProgress = DyInt(0)
        self.message = DyStr("")

    def setupTriggers(self):
        pass


class EM(ExecutionManager):
    def setupThreads(self):
        self.PyQt = DyThread()
        self.MainUI = DyThread()
        self.Exam = DyThread()


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.Skull.Features import ExaminationFeature
        from FTV.Extra.Examples.Skull.Features import ExaminationWindowFeature

        self.addFeature(ExaminationFeature)
        self.addFeature(ExaminationWindowFeature)


class SkullApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)
        self.setVariableManager(VM)
