import re
import time

from Objects.Communication import SerialManager, Port
from Objects.Data.Devices import Device
from Objects.Data.Examination import ExamManager
from Objects.Listeners.Senders import DeviceSender
from Objects.Services.Services import Service


class DeviceService(Service):
    def __init__(self, port: Port):
        super(DeviceService, self).__init__()
        self.port: Port = port
        self.del_t = 0
        self.deviceSender = DeviceSender(self)

    def setup(self):
        self.connect()

    def loop(self):
        if self.isAlive():
            sensor_params = self.getSensorDataFromDevice()

            # Print the collected sensor data
            self.print(f"{self.port.getPortName()}: \033[0;33m{sensor_params}\033[0m")

            self.sendSensorDataToUI(sensor_params)
        else:
            self.deviceSender.onDeviceDisconnected(self)
            return False

    def isAlive(self):
        return self.port.isAlive()

    def connect(self):
        self.port.connect()
        # TODO lahav please add an exception mechanism for the communication with the physical device.
        self.deviceSender.onDeviceConnected(self)

    def sensorDataToParams(self, sen_data):
        sen_data_list = [item.split("data:")[-1] for item in sen_data.split("\n")]

        res = []

        for data in sen_data_list:
            items = [item.split(":", 1) for item in data.split("@")]
            data_dict = {}

            for item in items:
                key = item[-2]
                value = item[-1]

                if key in ("power", "dtr", "mV"):
                    value = int(value)

                data_dict[key] = value

            res.append(data_dict)

        return res

    def getSensorDataFromDevice(self):
        return self.sensorDataToParams(
            self.port.getSensorData()
        )

    def sendSensorDataToUI(self, data):
        self.sensors_shared.put(data)

    def completeCurrentIteration(self):
        pass

    def saveDataLocally(self):
        pass

    def sendTimeoutError(self):
        pass

    def onWindowClosed(self):
        self.completeCurrentIteration()
        self.saveDataLocally()

    def onCommunicationTimeout(self):
        self.sendTimeoutError()

    def onDeviceConnected(self, device):
        pass

    def onDeviceDisconnected(self, device):
        pass

    def setOnWindowClosed(self, target):
        self.onWindowClosed = target

    def setOnCommunicationTimeout(self, target):
        self.sendTimeoutError = target

    def setOnDeviceConnected(self, target):
        self.onDeviceConnected = target

    def setOnDeviceDisconnected(self, target):
        self.onDeviceDisconnected = target


class DeviceManagerService(Service):
    def __init__(self):
        super(DeviceManagerService, self).__init__()
        self.devices: list[Device] = []
        self.serialManager = SerialManager(baudrate=921600)
        self.examManager = ExamManager()
        self.deviceSender = DeviceSender(self)

    def setup(self):
        # time.sleep(1)  # TODO lahav this line ensures that the device is connected only after the UI is up.
        # setup device properties
        pass

    def loop(self):
        # self.print("is device available")
        if self.isDeviceAvailable():
            self.print("Found a device!")
            port = self.serialManager.getAvailablePort()
            self.startDeviceThread(port)

    def isDeviceAvailable(self):
        self.serialManager.scanPorts()
        return self.serialManager.isPortAvailable()

    def startDeviceThread(self, port):
        time.sleep(1)  # TODO lahav this line ensures that the device is connected only after the UI is up.
        self.print(f"Connecting to port '{port}'")

        # Get device info

        # Create the device service
        deviceService = DeviceService(port)
        deviceService.setAsThread()
        deviceService.setDel_t(1.5)
        deviceService.setOnDeviceConnected(self.deviceSender.onDeviceConnected)
        deviceService.setOnDeviceDisconnected(self.deviceSender.onDeviceDisconnected)

        # Start device service thread
        deviceService.start(
            (self.sensors_shared, self.sensors_lock)
            # (self.events_shared, self.events_lock)
        )

    def completeCurrentIteration(self):
        pass

    def saveDataLocally(self):
        pass

    def closeDeviceThread(self):
        pass

    def closeCurrentThread(self):
        pass

    def onWindowClosed(self):
        self.completeCurrentIteration()
        self.saveDataLocally()
        self.closeDeviceThread()
        self.closeCurrentThread()

    def onDeviceConnected(self, device: DeviceService):
        # TODO architecture please define if this function should be used instead of using the loop or in parallel.
        #  It can also be called from the loop itself.

        # Add device to a list
        self.devices.append(device)
        self.print(f"{device.port.getPortName()}: Connected!")

        # Trigger all listeners
        super().onDeviceConnected(device)

    def onDeviceDisconnected(self, device: DeviceService):
        self.devices.remove(device)
        self.print(f"{device.port.getPortName()}: Disconnected!")

        self.completeCurrentIteration()
        self.saveDataLocally()
        self.closeDeviceThread()


if __name__ == '__main__':
    service = DeviceService(Port("VIR1"))
    service.setup()
