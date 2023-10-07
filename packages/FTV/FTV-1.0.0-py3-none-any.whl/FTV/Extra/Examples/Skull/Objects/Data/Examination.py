import time
from threading import Thread

from Objects.Listeners.Receivers import DeviceReceiver, ExamReceiver
from Objects.Listeners.Senders import ExamSender


class FieldData:
    def __init__(self):
        self.label = ""
        self.value = ""
        self.options = None


class ExamData:
    def __init__(self):
        self.fields = []

    def addField(self, field):
        pass

    def setField(self, field):
        pass

    def addMetaData(self, meta):
        pass

    def setMetaData(self, meta):
        pass


class Exam(ExamReceiver):
    def __init__(self):
        self.thread: Thread = None
        self.exam_data: ExamData = None
        self.duration: int = None
        self.dir_name: str = None
        self.timestamp_dir_name: str = None
        self.file_names: list[str] = None
        self.is_canceled = False
        self.is_completed = False

        self.examSender = ExamSender(self)
        self.setup()

    def setup(self):
        super().setupListeners()

    def setDuration(self, duration):
        self.duration = duration

    def setPath(self, path):
        self.path = path

    def _run(self, *args):
        # TODO architecture start_exam()
        self._startExamRecord()

        if not self.is_canceled:
            self.examSender.onSendExamStarted()
            self._uploadExam()

    def _startExamRecord(self):
        # Perform exam here
        n = 3
        for i in range(n):
            if self.is_canceled:
                self.is_canceled = False
                break

            time.sleep(0.1)
            progress = int(100 * (i + 1) / n * 0.5)
            # Thread(target=self.examSender.onRecordProgressUpdate, args=(progress,)).start()
            self.examSender.onRecordProgressUpdate(progress)

        if self.is_canceled:
            print("exam record canceled")
        else:
            print("exam record completed :)")
            # Thread(target=self.examSender.onRecordCompleted).start()
            # self.examSender.onRecordCompleted()

    def _uploadExam(self):
        # Save the results to a file
        print("upload exam to DB")
        # Perform exam here
        n = 10
        for i in range(n):
            if self.is_canceled:
                self.is_canceled = False
                break

            time.sleep(0.25)
            progress = int(100 * (n + i + 1) / n * 0.5)
            # Thread(target=self.examSender.onSendExamProgressUpdate, args=(progress,)).start()
            self.examSender.onRecordProgressUpdate(progress)
            print(self.is_canceled)

        if self.is_canceled:
            print("send exam canceled")
        else:
            print("send exam completed :)")
            # Thread(target=self.examSender.onSendExamCompleted).start()
            self.is_completed = True
            self.examSender.onSendExamCompleted()

    def start(self):
        self.is_canceled = False
        self.is_completed = False
        self.thread = Thread(target=self._run, args=())
        self.thread.start()

    def cancel(self):
        if self.is_completed:
            print(f"close()")
        else:
            self.is_canceled = True
            print(f"cancel(): {self.is_canceled}")

    def updateData(self):
        pass

    def generateResult(self):
        pass

    def saveResult(self):
        pass

    def sendResult(self):
        pass

    def deleteResult(self):
        pass

    def setExamData(self, exam_data):
        self.exam_data = exam_data

    def onRecordStarted(self):
        pass

    def onExamCanceled(self):
        pass

    def onRecordFailure(self):
        pass

    def onRecordCompleted(self):
        # Thread(target=self.examSender.onSendExamStarted).start()
        self.examSender.onSendExamStarted()

    def onRecordProgressUpdate(self, progress):
        pass

    def onSendExamStarted(self):
        pass
        # self._uploadExam()

    def onSendExamFailure(self):
        pass

    def onSendExamCompleted(self):
        pass


class ExamManager(DeviceReceiver, ExamReceiver):
    def __init__(self):
        super().__init__()
        self.exams: list[Exam] = []
        self.result_dir: str = None
        self.setup()

    def setup(self):
        super().setupListeners()

    # @classmethod
    def setResultDir(self, result_dir):
        self.result_dir = result_dir

    # @classmethod
    def loadExam(self, path):
        pass

    # @classmethod
    def startExam(self):
        print(f"Starting an exam")

        # Create the exam service
        self.exam = Exam()
        self.exams.append(self.exam)

        self.exam.start()
        print([item.thread.is_alive() for item in self.exams])

    # @classmethod
    def cancelExam(self):
        self.exam.cancel()

    def onSensorsDataUpdated(self, sensors_data):
        pass

    def onDeviceDisconnected(self, device):
        pass

    def onDeviceConnected(self, device):
        pass

    def onRecordStarted(self):
        self.startExam()

    def onExamCanceled(self):
        self.cancelExam()

    def onRecordFailure(self):
        pass

    def onRecordCompleted(self):
        pass

    def onRecordProgressUpdate(self, progress):
        pass

    def onSendExamStarted(self):
        pass

    def onSendExamFailure(self):
        pass

    def onSendExamCompleted(self):
        pass

    def onSendExamProgressUpdate(self, progress):
        pass

