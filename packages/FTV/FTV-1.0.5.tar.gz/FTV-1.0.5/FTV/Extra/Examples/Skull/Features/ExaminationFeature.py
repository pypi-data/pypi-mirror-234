import time

from FTV.Extra.Examples.Skull.SkullApp import SkullApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod


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


class ExaminationFeature(NIFeature):
    def __init__(self):
        super(ExaminationFeature, self).__init__()
        self.is_canceled = False

    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(self.vm.onWindowOpened).setAction(self.startExam)\
            .setThread(SkullApp.em.Exam)

        self.addTrigger(self.vm.onRecordStarted).setAction(self.startRecord)
        self.addTrigger(self.vm.onRecordCompleted).setAction(self.vm.onSendExamStarted)

        self.addTrigger(self.vm.onSendExamStarted).setAction(self.startSendExam)
        # self.addTrigger(self.vm.onSendExamCompleted).setAction(self.)

        self.addTrigger(self.vm.onExamCancelRequested).setAction(self.cancelExam)
        self.addTrigger(self.vm.onWindowClosed).setAction(self.cancelExam)

    @DyMethod()
    def startExam(self):
        self.vm.onRecordStarted.activate()

    @DyMethod()
    def startRecord(self):
        # Perform exam here
        self.vm.message.set("Recording...")
        n = 3
        for i in range(n):
            if self.is_canceled:
                self.is_canceled = False
                break

            time.sleep(0.1)
            progress = int(100 * (i + 1) / n)
            self.vm.recordProgress.set(progress)

        if self.is_canceled:
            Log.p("exam record canceled")
            self.vm.onExamCanceled.activate()
        else:
            Log.p("exam record completed :)")
            self.vm.onRecordCompleted.activate()

    @DyMethod()
    def startSendExam(self):
        # Save the results to a file
        Log.p("upload exam to DB")
        self.vm.message.set("Uploading...")
        # Perform exam here
        n = 10
        for i in range(n):
            if self.is_canceled:
                self.is_canceled = False
                break

            time.sleep(0.25)
            progress = int(100 * (i + 1) / n)
            # Thread(target=self.examSender.onSendExamProgressUpdate, args=(progress,)).start()
            self.vm.uploadProgress.set(progress)

        if self.is_canceled:
            Log.p("send exam canceled")
            self.vm.onExamCanceled.activate()
        else:
            Log.p("send exam completed :)")
            # Thread(target=self.examSender.onSendExamCompleted).start()
            self.vm.message.set("Exam completed.")
            self.vm.onSendExamCompleted.activate()

    @DyMethod()
    def cancelExam(self):
        self.is_canceled = True
