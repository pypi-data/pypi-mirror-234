import sys

from PyQt5.QtWidgets import QApplication

from FTV.Extra.Examples.Skull.Objects import ExaminationWindow
from FTV.Extra.Examples.Skull.SkullApp import SkullApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod


class VM(VariableManager):
    def setupVariables(self):
        self.onRecordStarted = SkullApp.vm.onRecordStarted
        self.onExamCancelRequested = SkullApp.vm.onExamCancelRequested
        self.onExamCanceled = SkullApp.vm.onExamCanceled

        self.onRecordFailure = SkullApp.vm.onRecordFailure
        self.onRecordCompleted = SkullApp.vm.onRecordCompleted
        self.onRecordProgressUpdate = SkullApp.vm.onRecordProgressUpdate
        self.onSendExamStarted = SkullApp.vm.onSendExamStarted
        self.onSendExamFailure = SkullApp.vm.onSendExamFailure
        self.onSendExamCompleted = SkullApp.vm.onSendExamCompleted
        self.onSendExamProgressUpdate = SkullApp.vm.onSendExamProgressUpdate

        self.onWindowOpened = SkullApp.vm.onWindowOpened
        self.onWindowClosed = SkullApp.vm.onWindowClosed

        self.recordProgress = SkullApp.vm.recordProgress
        self.uploadProgress = SkullApp.vm.uploadProgress
        self.message = SkullApp.vm.message

    def setupTriggers(self):
        pass


class ExaminationWindowFeature(NIFeature):
    def __init__(self):
        super().__init__()
        # self.window = ExaminationWindow()

        # app = QApplication(sys.argv)
        # self.window = QWidget()
        # sys.exit(app.exec_())

    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(SkullApp.vm.START).setAction(self.openWindow)\
            .setThread(SkullApp.em.PyQt)

        self.addTrigger(self.vm.recordProgress).setAction(self.updateRecordProgress)\
            .setThread(SkullApp.em.MainUI)
        self.addTrigger(self.vm.uploadProgress).setAction(self.updateUploadProgress)\
            .setThread(SkullApp.em.MainUI)

        self.addTrigger(self.vm.message).setAction(self.updateMessage)
        self.addTrigger(self.vm.onExamCanceled).setAction(self.closeWindow)

    @DyMethod()
    def openWindow(self):
        app = QApplication(sys.argv)
        self.window = ExaminationWindow()

        self.window.onClose = self.onClose

        self.window.start()
        self.window.show()
        self.vm.onWindowOpened.activate()
        sys.exit(app.exec_())
        Log.p("App is closed.")

    @DyMethod()
    def updateRecordProgress(self):
        self.window.updateExamProgress(self.vm.recordProgress)

    @DyMethod()
    def updateUploadProgress(self):
        self.window.updateSendExamProgress(self.vm.uploadProgress)

    @DyMethod()
    def updateMessage(self):
        self.window.updateMessage(self.vm.message)

    @DyBuiltinMethod()
    def onClose(self):
        self.vm.onExamCancelRequested.activate()
        self.vm.onWindowClosed.activate()
        # Log.p("Closing the window")

    @DyMethod()
    def closeWindow(self):
        self.window.hide()
