from Objects.Listeners.Receivers import DeviceReceiver
from Objects.UI.Fields.BaseFields import MultiComboboxField, TextboxField, CheckboxTextboxGroupField, SubTextboxField, \
    RadioButtonsField, TextboxGroupField, ComboboxField, CheckboxField


class PainLocationField(MultiComboboxField):
    def label(self):
        return "Pain Location"

    def default(self):
        return []

    def options(self):
        return [
            "Across",
            "Center",
            "Rt.",
            "Lt.",
            "Buttock Lt.",
            "Buttock Rt.",
            "Hip Lt.",
            "Hip Rt.",
            "Knee Lt.",
            "Knee Rt.",
            "Leg Lt.",
            "Leg Rt.",
            "Ankle Lt.",
            "Ankle Rt.",
            "Foot/Heel Lt.",
            "Foot/Heel Lt.",
            "No"
        ]

    def max_columns(self):
        return 3


class RadiatingPainField(MultiComboboxField):
    def label(self):
        return "Radiating Pain"

    def default(self):
        return []

    def options(self):
        return [
            "No",
            "Lt.",
            "Rt.",
            "Bilateral"
        ]

    def max_columns(self):
        return 3


class PainLevelField(TextboxField):
    def label(self):
        return "Pain Level"

    def default(self):
        return "0"


class RateField(TextboxField):
    def label(self):
        return "Rate"

    def default(self):
        return "4.2"


class PLEField(CheckboxTextboxGroupField):
    def label(self):
        return "PLE"

    def subFields(self):
        return [
            (PLEField.Lt, False),
            (PLEField.Rt, False)
        ]

    class Lt(SubTextboxField):
        def label(self):
            return "°Lt"

        def default(self):
            return "0"

    class Rt(SubTextboxField):
        def label(self):
            return "°Rt"

        def default(self):
            return "0"


class ShortLegField(RadioButtonsField):
    def label(self):
        return "Short Leg"

    def default(self):
        return "No"

    def options(self):
        return [
            "No",
            "Lt",
            "Rt"
        ]


class GaitFailureField(RadioButtonsField):
    def label(self):
        return "Gait Failure"

    def default(self):
        return "No"

    def options(self):
        return [
            "No",
            "Lt",
            "Rt"
        ]


class DominantSideField(RadioButtonsField):
    def label(self):
        return "Dominant Side"

    def default(self):
        return "R"

    def options(self):
        return [
            "L",
            "R"
        ]


class PPressureField(TextboxGroupField):

    def label(self):
        return "P.Pressure"

    # def default(self):
    #     pass

    def subFields(self):
        return [
            PPressureField.Lt,
            PPressureField.Rt
        ]

    class Lt(SubTextboxField):
        def label(self):
            return "Lt"

        def default(self):
            return "0"

    class Rt(SubTextboxField):
        def label(self):
            return "Rt"

        def default(self):
            return "0"


class SeverityEstField(ComboboxField):
    def label(self):
        return "Severity Est"

    def default(self):
        return "None"

    def options(self):
        return [
            "Mild",
            "Moderate",
            "Severe",
            "None"
        ]


class OutlierSuspectField(CheckboxField):
    def label(self):
        return "Outlier Suspect"

    def default(self):
        return False


class MedicatedField(CheckboxField):
    def label(self):
        return "Medicated"

    def default(self):
        return False


class PortSerialField(ComboboxField, DeviceReceiver):
    def __init__(self):
        super().__init__()
        self.port_names = []
        self.setup()

    def setup(self):
        super().setupListeners()

    def label(self):
        return "Port Serial"

    def default(self):
        return None

    def options(self):
        return []

    def onDeviceConnected(self, device):
        self.port_names.append(device.port.getPortName())

        self.updatePortList()

    def onDeviceDisconnected(self, device):
        self.port_names.remove(device.port.getPortName())

        self.updatePortList()

    def onSensorsDataUpdated(self, sensors_data):
        pass

    def updatePortList(self):
        self.setValueOptions(self.port_names)
