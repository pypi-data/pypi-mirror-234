import sys
from abc import abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QShowEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QApplication

from FTV.Extra.Examples.Skull.Objects import DeviceReceiver, ExamReceiver
from FTV.Extra.Examples.Skull.Objects import ExamSender
from FTV.Extra.Examples.Skull.Objects import Button
from FTV.Extra.Examples.Skull.Objects import GroupBox
from FTV.Extra.Examples.Skull.Objects.UI import Label
from FTV.Extra.Examples.Skull.paths import ICON_DIR


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.app_style = "Breeze"
        self.icon_dir = None

    def setIconDir(self, icon_dir):
        self.icon_dir = icon_dir

    def showEvent(self, a0: QShowEvent) -> None:
        res = self.onOpen()
        if res is False:
            a0.ignore()
        else:
            a0.accept()

    def closeEvent(self, a0: QCloseEvent) -> None:
        res = self.onClose()
        if res is False:
            a0.ignore()
        else:
            a0.accept()

    @abstractmethod
    def onOpen(self):
        pass

    @abstractmethod
    def onClose(self):
        pass


class ExaminationWindow(Window, DeviceReceiver, ExamReceiver):
    def __init__(self):
        super().__init__()
        self.examSender = ExamSender(self)

        self.setup()

    def start(self):
        self.setWindowTitle("Examination")
        self.setFixedWidth(400)

        # Set default icon dir
        Button.setIconDir(self.icon_dir)

        self.record_label = Label()
        self.record_progressbar = QProgressBar()
        self.record_progressbar.setValue(0)

        # Create exam progress layout
        self.record_layout = QHBoxLayout()
        self.record_layout.addWidget(self.record_label)
        self.record_layout.addWidget(self.record_progressbar)

        self.send_exam_label = Label()
        self.send_exam_progressbar = QProgressBar()
        self.send_exam_progressbar.setValue(0)

        # Create send report layout
        self.send_exam_layout = QHBoxLayout()
        self.send_exam_layout.addWidget(self.send_exam_label)
        self.send_exam_layout.addWidget(self.send_exam_progressbar)

        self.response_label = Label()

        self.response_layout = QHBoxLayout()
        self.response_layout.addWidget(self.response_label)

        self.response_groupbox = GroupBox()
        self.response_groupbox.setLayout(self.response_layout)

        # Create response layout
        self.response_layout = QHBoxLayout()
        self.response_layout.addWidget(self.response_groupbox)

        # Create close button
        self.close_btn = Button("Close")
        self.close_btn.setFixedWidth(70)
        self.close_btn.clicked.connect(self.close)

        # Create close layout
        self.close_layout = QHBoxLayout()
        self.close_layout.addWidget(self.close_btn)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(self.record_layout)
        main_layout.addLayout(self.send_exam_layout)
        main_layout.addLayout(self.response_layout)
        main_layout.addLayout(self.close_layout)

        self.setLayout(main_layout)

    def setup(self):
        super().setupListeners()

    def setupDefaultUI(self):
        self.record_label.setText("Record: ")
        self.send_exam_label.setText("Upload: ")
        self.response_label.setText("")

        self.record_progressbar.setValue(0)
        self.send_exam_progressbar.setValue(0)

    def updateExamProgress(self, progress):
        self.record_progressbar.setValue(progress)

    def updateSendExamProgress(self, progress):
        self.send_exam_progressbar.setValue(progress)

    def onOpen(self):
        pass

    def onClose(self):
        pass

    def onSensorsDataUpdated(self, sensors_data):
        pass

    def onDeviceDisconnected(self, device):
        # print("Should close this window")
        # for i in range(5):
        if self.isVisible():
            print("close examination window")
            self.close()
        # try:
        #     self.close()
        # except Exception as e:
        #     print("close examination window error")
        #     raise e

    def onDeviceConnected(self, device):
        pass

    def onRecordProgressUpdate(self, progress):
        self.updateExamProgress(progress)

    def onRecordStarted(self):
        self.setupDefaultUI()
        self.response_label.setText("Recording...")

    def onExamCanceled(self):
        pass

    def onRecordFailure(self):
        pass

    def onRecordCompleted(self):
        pass

    def onSendExamStarted(self):
        self.response_label.setText("Uploading...")

    def onSendExamFailure(self):
        pass

    def onSendExamCompleted(self):
        self.response_label.setText("Upload completed.")

    def onSendExamProgressUpdate(self, progress):
        self.updateSendExamProgress(progress)

    def updateMessage(self, message):
        self.response_label.setText(message.get())


if __name__ == '__main__':
    # with AppRunner() as ar:
    app = QApplication(sys.argv)
    window = ExaminationWindow()
    window.setIconDir(ICON_DIR)
    window.start()
    # ar.setApp(window)
    window.show()


    # app = QApplication(sys.argv)
    # MainWindow()
    # app.start()
    # app.exec_()
