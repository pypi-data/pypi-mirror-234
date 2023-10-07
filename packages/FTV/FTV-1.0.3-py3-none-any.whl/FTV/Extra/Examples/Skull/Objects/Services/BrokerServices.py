import os

from Objects.Services.Services import Service
from Tools.Files import Json
from paths import STATIC_DATA_DIR


class CMD:
    StartLogger = "0"
    StopLogger = "1"
    BroadcastBrokerMAC = "7"
    GetDetails = "8"
    StoreLeftMAC = "4"
    StoreRightMAC = "5"
    StoreBackMAC = "6"


class VirtualBrokerService(Service):
    def __init__(self):
        super(VirtualBrokerService, self).__init__()
        self.sensors_path: str = None

    def setSensorsPath(self, sensors_path):
        self.sensors_path = sensors_path

    def start(self):
        self.print(f"Service is running [{os.getpid()}]")

        self.setup()
        self._startLoop()

    def setup(self):
        print("setup...")

    def loop(self):
        cmd = self.getCMD()
        message = None

        if cmd == CMD.StartLogger:
            pass
        elif cmd == CMD.StopLogger:
            pass
        elif cmd == CMD.BroadcastBrokerMAC:
            message = self.broadcastBrokerMAC()
        elif cmd == CMD.GetDetails:
            pass
        elif cmd == CMD.StoreLeftMAC:
            pass
        elif cmd == CMD.StoreRightMAC:
            pass
        elif cmd == CMD.StoreBackMAC:
            pass
        else:
            print(">>> Got the heck: ")
            print(cmd)
            message = f"Command '{cmd}' is not supported."

        if message is not None:
            self.sendResponse(message)

    def getCMD(self):
        pass

    def startLogger(self):
        pass

    def stopLogger(self):
        pass

    def broadcastBrokerMAC(self):
        sensors = Json.read(self.sensors_path)
        return Json.dumps(sensors)

    def getDetails(self):
        pass

    def storeSensorMAC(self, sensor_name):
        pass

    def sendResponse(self, message):
        pass


if __name__ == '__main__':
    service = VirtualBrokerService()
    service.setSensorsPath(STATIC_DATA_DIR + "sensors.json")
    service.start()
