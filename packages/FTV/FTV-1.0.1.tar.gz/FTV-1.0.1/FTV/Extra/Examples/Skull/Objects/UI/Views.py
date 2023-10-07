from abc import abstractmethod

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout

from Objects.Listeners.Receivers import DeviceReceiver, ExamReceiver
from Objects.Listeners.Senders import ExamSender
from Objects.UI.Buttons import Button, ActionButton
from Objects.UI.CheckBoxes import CheckBox
from Objects.UI.Fields.ExaminationFields import PainLocationField, RadiatingPainField, PainLevelField, RateField, \
    PLEField, ShortLegField, GaitFailureField, DominantSideField, PPressureField, SeverityEstField, OutlierSuspectField, \
    MedicatedField, PortSerialField
from Objects.UI.Fields.PatientFields import PatientCodeField, SubluxationTagField, TrainingExamField, GenderField, \
    WeightGroupField, AgeField, DataDurationField, NotesField
from Objects.UI.FormLayouts import PatientFormLayout, ExaminationFormLayout
from Objects.UI.Graphs import Graph
from Objects.UI.GroupBox import GroupBox
from Objects.UI.Images import Image
from Objects.UI.Labels import Label
from Objects.UI.LineEdits import LineEdit
from Objects.UI.Sliders import Slider
from paths import ICON_DIR

matplotlib.use('Qt5Agg')


class Section:
    def setup(self):
        self.setupDefaultUI()
        self.setupEvents()

    @abstractmethod
    def setupDefaultUI(self):
        pass

    @abstractmethod
    def setupEvents(self):
        pass


class SensorSection(Section, QHBoxLayout, DeviceReceiver):
    def __init__(self):
        super().__init__()
        # TODO architecture Please build the sensors representation according the the design philosophy.

        sensor_names = [
            "Left Sensor",
            "Back Sensor",
            "Right Sensor"
        ]

        self.sensors_data: [dict] = None

        self.setSpacing(30)
        self.setAlignment(Qt.AlignCenter)

        self.signal_dir = ICON_DIR + "signal/"
        self.battery_dir = ICON_DIR + "battery/"
        self.general_dir = ICON_DIR + "general/"

        self.signal_images = []
        self.battery_images = []

        for sensor_name in sensor_names:
            signal_label = Label("Signal:")
            signal_image = Image()
            self.signal_images.append(signal_image)

            signal_layout = QFormLayout()
            signal_layout.addRow(signal_label, signal_image)
            signal_layout.setSpacing(20)

            battery_label = Label("Battery:")
            battery_image = Image()
            self.battery_images.append(battery_image)

            battery_layout = QFormLayout()
            battery_layout.addRow(battery_label, battery_image)
            battery_layout.setSpacing(20)

            layout = QVBoxLayout()
            layout.addLayout(signal_layout)
            layout.addLayout(battery_layout)

            sensor_group_box = GroupBox(sensor_name)
            sensor_group_box.setLayout(layout)

            self.addWidget(sensor_group_box)

    def setup(self):
        super().setup()
        super().setupListeners()

    def setupDefaultUI(self):
        self.updateBatteries()
        self.updateSignals()

    def setupEvents(self):
        pass

    def updateBatteries(self):
        dir = self.general_dir
        icon = "nc.jpg"
        alignment = Qt.AlignRight

        if self.sensors_data is None:
            self.sensors_data = [None]*len(self.battery_images)

        for image, sensor_data in zip(self.battery_images, self.sensors_data):
            if sensor_data is not None:
                # noinspection PyUnresolvedReferences
                data = sensor_data["power"]
                dir = self.battery_dir
                alignment = Qt.AlignCenter

                index = round(100.0 / int(data)) + 1 if data else 0
                icon = f"b{index}.gif"

            image.setSource(dir + icon)
            image.setAlignment(alignment)

    def updateSignals(self):
        dir = self.general_dir
        icon = "nc.jpg"
        alignment = Qt.AlignRight

        if self.sensors_data is None:
            self.sensors_data = [None]*len(self.signal_images)

        for image, sensor_data in zip(self.signal_images, self.sensors_data):
            if sensor_data is not None:
                # noinspection PyUnresolvedReferences
                data = sensor_data["mV"]
                dir = self.signal_dir
                alignment = Qt.AlignCenter

                index = round((int(data) - 3200) * 3 / 1200) + 1 if data else 0
                icon = f"s{index}.gif"

            image.setSource(dir + icon)
            image.setAlignment(alignment)

    def updateSensorsData(self, sensors_data):
        self.sensors_data = sensors_data
        # TODO architecture-done update_ui_by_sensors()
        self.updateBatteries()
        self.updateSignals()

    def onSensorsDataUpdated(self, sensors_data):
        self.updateSensorsData(sensors_data)

    def onDeviceDisconnected(self, device):
        self.updateSensorsData(None)

    def onDeviceConnected(self, device):
        pass


class DataAcquisitionSection(Section, QVBoxLayout, DeviceReceiver, ExamReceiver):
    def __init__(self):
        super().__init__()

        self.patient_form_layout = PatientFormLayout(
            PatientCodeField,
            SubluxationTagField,
            TrainingExamField,
            GenderField,
            WeightGroupField,
            AgeField,
            DataDurationField,
            NotesField
        )
        self.patient_identifiers = GroupBox("Patient Identifiers")
        self.patient_identifiers.setLayout(self.patient_form_layout)

        self.examination_form_layout = ExaminationFormLayout(
            PainLocationField,
            RadiatingPainField,
            PainLevelField,
            RateField,
            PLEField,
            ShortLegField,
            GaitFailureField,
            DominantSideField,
            PPressureField,
            SeverityEstField,
            OutlierSuspectField,
            MedicatedField,
            PortSerialField
        )
        self.examination_metrics = GroupBox("Examination Metrics")
        self.examination_metrics.setLayout(self.examination_form_layout)

        self.examination_details_layout = QHBoxLayout()
        self.examination_details_layout.addWidget(self.patient_identifiers)
        self.examination_details_layout.addWidget(self.examination_metrics)

        self.examination_details_group = GroupBox("Examination Details")
        self.examination_details_group.setLayout(self.examination_details_layout)

        self.sensors_layout = SensorSection()
        self.sensors_layout.setContentsMargins(0,10,0,10)

        self.start_btn = ActionButton("Start")
        self.abort_btn = ActionButton("Abort")

        self.actions_layout = QHBoxLayout()
        self.actions_layout.setAlignment(Qt.AlignCenter)
        self.actions_layout.setSpacing(50)
        self.actions_layout.setContentsMargins(0,10,0,10)
        self.actions_layout.addWidget(self.start_btn)
        self.actions_layout.addWidget(self.abort_btn)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.examination_details_group)
        self.layout.addLayout(self.sensors_layout)
        self.layout.addLayout(self.actions_layout)

        self.addLayout(self.layout)

        from Objects.UI.Windows import ExaminationWindow

        self.exam_window = ExaminationWindow()
        self.exam_window.setWindowModality(Qt.ApplicationModal)
        self.exam_window.start()

        self.examSender = ExamSender(self)

    def setup(self):
        super().setup()
        self.sensors_layout.setup()

        super().setupListeners()

    def setupDefaultUI(self):
        self.is_device_connected = False
        self.updateStartButton()

    def setupEvents(self):
        self.start_btn.clicked.connect(lambda: self.examSender.onRecordStarted())

        for field in self.patient_form_layout.getCriticalFields():
            if "changed" in dir(field):
                field.changed.connect(lambda: self.updateStartButton())

    def onSensorsDataUpdated(self, sensors_data):
        pass

    def onDeviceDisconnected(self, device):
        self.is_device_connected = False
        self.updateStartButton()

    def onDeviceConnected(self, device):
        self.is_device_connected = True
        self.updateStartButton()

    def onRecordStarted(self):
        self.openExamWindow()

    def onExamCanceled(self):
        pass

    def onRecordFailure(self):
        pass

    def onRecordProgressUpdate(self, progress):
        pass

    # TODO architecture-done update_start_button()
    def updateStartButton(self):
        # Disable Start button if no sensors detected
        enabled = self.patient_form_layout.areCriticalFieldsFull() and self.is_device_connected
        self.start_btn.setEnabled(enabled)

    def updateStartButtonFieldsChanged(self, enabled):
        self.start_btn.setEnabled(enabled)

    def openExamWindow(self):
        self.exam_window.show()


class AnalysisDataGroup(GroupBox):
    def __init__(self, *args, button_text="", label_text="Nothing loaded"):
        super().__init__(*args)

        self.show_checkbox = CheckBox("Show")
        self.load_exam_btn = Button(button_text)
        self.label = Label(label_text)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setSpacing(15)
        self.layout.addWidget(self.show_checkbox)
        self.layout.addWidget(self.load_exam_btn)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


class AnalysisFilterGroup(GroupBox):
    def __init__(self, *args, checkbox_texts=None, upper=False):
        super().__init__(*args)
        self.checkboxes = []

        self.layout = QHBoxLayout()
        self.layout.setSpacing(15)

        for checkbox_text in checkbox_texts:
            if upper:
                checkbox_text = checkbox_text.upper()

            checkbox = CheckBox(checkbox_text)
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.setLayout(self.layout)


class AnalysisSection(Section, QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.analysis_data_group_1 = AnalysisDataGroup("StaticData 1", button_text="Load exam 1")
        self.analysis_data_group_2 = AnalysisDataGroup("StaticData 2", button_text="Load exam 2")

        self.data_layout = QHBoxLayout()
        self.data_layout.addWidget(self.analysis_data_group_1)
        self.data_layout.addWidget(self.analysis_data_group_2)

        self.analysis_filter_group_accel = AnalysisFilterGroup("Accel",
                                                               checkbox_texts=("all", "x", "y", "z"),
                                                               upper=True)
        self.analysis_filter_group_gyro = AnalysisFilterGroup("Gyro",
                                                              checkbox_texts=("all", "x", "y", "z"),
                                                              upper=True)
        self.analysis_filter_group_magnet = AnalysisFilterGroup("Magnet",
                                                                checkbox_texts=("all", "x", "y", "z", "h"),
                                                                upper=True)

        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 50)
        self.slider.setPageStep(50)

        self.slider_text_edit = LineEdit("1")
        self.slider_text_edit.setEnabled(False)
        self.slider_text_edit.setAlignment(Qt.AlignCenter)
        self.slider_text_edit.setFixedWidth(30)

        self.slider_layout = QHBoxLayout()
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.slider_text_edit)

        self.filter_layout = QHBoxLayout()
        self.filter_layout.addWidget(self.analysis_filter_group_accel)
        self.filter_layout.addWidget(self.analysis_filter_group_gyro)
        self.filter_layout.addWidget(self.analysis_filter_group_magnet)
        self.filter_layout.addLayout(self.slider_layout)

        self.chart_settings_layout = QVBoxLayout()
        self.chart_settings_layout.addLayout(self.data_layout)
        self.chart_settings_layout.addLayout(self.filter_layout)

        self.chart_settings_group = GroupBox("Chart Settings")
        self.chart_settings_group.setLayout(self.chart_settings_layout)

        self.graph = Graph()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.chart_settings_group)
        self.layout.addWidget(self.graph)

        self.addLayout(self.layout)

    def setupDefaultUI(self):
        pass

    def setupEvents(self):
        self.slider.valueChanged.connect(self.updateSliderTextEdit)

    def updateSliderTextEdit(self, value):
        self.slider_text_edit.setText(str(value))


class ConsoleSection(Section, QVBoxLayout):
    def __init__(self):
        super().__init__()

        # self.addLayout(self.layout)

    def setupDefaultUI(self):
        pass

    def setupEvents(self):
        pass


class InstructionsBarSection(Section, GroupBox, DeviceReceiver):
    def __init__(self):
        super().__init__()

        self.instructions_label = Label()

        layout = QHBoxLayout()
        layout.addWidget(self.instructions_label)

        self.setLayout(layout)

    def setup(self):
        super().setup()
        super().setupListeners()

    def setupDefaultUI(self):
        self.updateStatusBar(False)

    def setupEvents(self):
        pass

    def updateStatusBar(self, state):
        if state:
            message = 'Click "Start" button to begin motion recording'
        else:
            message = 'Waiting for sensors presence...'

        self.instructions_label.setText(message)

    def onSensorsDataUpdated(self, sensors_data):
        pass

    def onDeviceDisconnected(self, device):
        self.updateStatusBar(False)

    def onDeviceConnected(self, device):
        self.updateStatusBar(True)
