from typing import Tuple

import numpy as np
from PyQt5.QtCore import QThread, QTimer

from Objects.Listeners.Senders import DeviceSender
from Objects.Services.Services import Service
from Objects.UI.General import AppRunner, Worker
from Objects.UI.Windows import MainWindow


class UIService(Service):
    def __init__(self):
        super(UIService, self).__init__()
        self.mainWindow: MainWindow
        self.icon_dir = ""

        # TODO lahav rename below block to avoid dependency between services
        self.map: Tuple[np.matrix, np.matrix] = None

        self.loop_graph_status: bool = True
        self.loop_canvas_status: bool = True

        self.deviceSender = DeviceSender(self)

    def setIconDir(self, icon_dir):
        self.icon_dir = icon_dir

    def start(self, *args):
        self._run(*args)

    def setup(self):
        with AppRunner() as ar:
            self.mainWindow = MainWindow()
            self.mainWindow.setIconDir(self.icon_dir)
            self.mainWindow.start()
            ar.setApp(self.mainWindow)

            self.setupGraph()

            self.getUIState()
            self.mainWindow.setup()

            # start thread "_startLoop()"
            self._startUILoop()

    def _startLoop(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._timer_loop)
        self.timer.start(self.del_t)

    def _startUILoop(self):
        self.thread = QThread()
        self.worker = Worker(self._startLoop)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def setupGraph(self):
        pass

    # TODO architecture-done update_ui_loop()
    def loop(self):
        # TODO architecture-done get_data_from_sensor()
        sensors_data = self.getSensorsData()
        self.print(f"\033[0;35m{sensors_data}\033[0m")
        self.deviceSender.onSensorsDataUpdated(sensors_data)

    def getUIState(self):
        pass

    def setupDefaultUI(self):
        pass

    def getSensorsData(self):
        return self.sensors_shared.get()

    def updateUIFormUser(self):
        pass

    def performAction(self):
        pass

    def saveCurrentState(self):
        pass

    def closeWindow(self):
        pass

    def onUIEvent(self):
        self.updateUIFormUser()
        self.performAction()

    def onWindowClosed(self):
        self.saveCurrentState()
        self.closeWindow()


if __name__ == '__main__':
    ui_services = UIService()
    ui_services.setup()

    # with AppRunner() as ar:
    #     app = MainWindow()
    #     app.start()
    #     ar.setApp(app)
