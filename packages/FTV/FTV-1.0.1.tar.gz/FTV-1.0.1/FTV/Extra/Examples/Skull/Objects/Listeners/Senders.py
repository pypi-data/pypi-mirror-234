from FTV.Extra.Examples.Skull.Objects import Sender, sender
from FTV.Extra.Examples.Skull.Objects import DeviceListener, ExamListener


class DeviceSender(Sender, DeviceListener):
    @sender()
    def onSensorsDataUpdated(self, sensors_data):
        # print("-> onSensorsDataUpdated()")
        pass

    @sender()
    def onDeviceConnected(self, device):
        print("-> onDeviceConnected()")
        pass

    @sender()
    def onDeviceDisconnected(self, device):
        print("-> onDeviceDisconnected()")
        pass


class ExamSender(Sender, ExamListener):
    @sender()
    def onRecordStarted(self):
        print("-> onRecordStarted()")
        pass

    @sender()
    def onExamCanceled(self):
        print("-> onExamCanceled()")
        pass

    @sender()
    def onRecordFailure(self):
        # print("-> onRecordFailure()")
        pass

    @sender()
    def onRecordCompleted(self):
        print("-> onRecordCompleted()")
        pass

    @sender()
    def onRecordProgressUpdate(self, progress):
        print(f"-> onRecordProgressUpdate({progress})")
        pass

    @sender()
    def onSendExamStarted(self):
        print("-> onSendExamStarted()")
        pass

    @sender()
    def onSendExamFailure(self):
        # print("-> onSendExamFailure()")
        pass

    @sender()
    def onSendExamCompleted(self):
        # print("-> onSendExamCompleted()")
        pass

    @sender()
    def onSendExamProgressUpdate(self, progress):
        print(f"-> onSendExamProgressUpdate({progress})")
        pass
