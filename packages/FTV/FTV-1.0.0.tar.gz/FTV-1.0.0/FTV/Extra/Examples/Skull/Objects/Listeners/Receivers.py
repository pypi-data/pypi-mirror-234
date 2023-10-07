from abc import abstractmethod

from FTV.Extra.Examples.Skull.Objects import Receiver
from FTV.Extra.Examples.Skull.Objects import DeviceListener, ExamListener


class DeviceReceiver(Receiver, DeviceListener):
    @abstractmethod
    def onSensorsDataUpdated(self, sensors_data):
        pass

    @abstractmethod
    def onDeviceDisconnected(self, device):
        pass

    @abstractmethod
    def onDeviceConnected(self, device):
        pass


class ExamReceiver(Receiver, ExamListener):
    @abstractmethod
    def onRecordStarted(self):
        pass

    @abstractmethod
    def onExamCanceled(self):
        pass

    @abstractmethod
    def onRecordFailure(self):
        pass

    @abstractmethod
    def onRecordCompleted(self):
        pass

    @abstractmethod
    def onRecordProgressUpdate(self, progress):
        pass

    @abstractmethod
    def onSendExamStarted(self):
        pass

    @abstractmethod
    def onSendExamFailure(self):
        pass

    @abstractmethod
    def onSendExamCompleted(self):
        pass

    @abstractmethod
    def onSendExamProgressUpdate(self, progress):
        pass
