from Objects.Data.Examination import Exam
from Objects.Services.Services import Service


class ExamService(Service):
    def __init__(self):
        super(ExamService, self).__init__()
        self.del_t = 0

    def setup(self):
        pass

    def loop(self):
        pass


class ExamManagerService(Service):
    def __init__(self):
        super(ExamManagerService, self).__init__()
        self.exams: list[Exam] = []

    def setup(self):
        pass

    def loop(self):
        return False
        # self.startDeviceThread()

    def startExamThread(self):
        # Create the exam service
        examService = ExamService()
        examService.setAsThread()
        examService.setDel_t(1.5)
        # examService.setOnDeviceConnected(self.onDeviceConnected)
        # examService.setOnDeviceDisconnected(self.onDeviceDisconnected)

        # Start exam service thread
        examService.start(
            (self.sensors_shared, self.sensors_lock)
            # (self.events_shared, self.events_lock)
        )


if __name__ == '__main__':
    service = ExamService()
    service.setup()
