from abc import abstractmethod


class DeviceListener:
    @abstractmethod
    def onSensorsDataUpdated(self, sensors_data):
        pass

    @abstractmethod
    def onDeviceDisconnected(self, device):
        pass

    @abstractmethod
    def onDeviceConnected(self, device):
        pass


class ExamListener:
    @abstractmethod
    def onRecordStarted(self):
        pass

    @abstractmethod
    def onExamCanceled(self):
        pass

    @abstractmethod
    def onRecordFailure(self):
        pass
