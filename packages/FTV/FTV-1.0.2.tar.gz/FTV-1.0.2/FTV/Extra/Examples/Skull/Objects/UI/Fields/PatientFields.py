from Objects.UI.Fields.BaseFields import TextboxField, ComboboxField, RadioButtonsField, ScrollableTextboxField


class PatientCodeField(TextboxField):
    def label(self):
        return "Patient Code"

    def default(self):
        return ""

    def critical(self):
        return True


class SubluxationTagField(ComboboxField):
    def label(self):
        return "Subluxation Tag"

    def default(self):
        return ""

    def options(self):
        return [
            "",
            "Normal",
            "LT-PI/RT-AS",
            "LT-AS/RT-PI",
            "RT-PI",
            "RT-AS",
            "LT-PI",
            "LT-AS"
        ]

    def critical(self):
        return True


class TrainingExamField(RadioButtonsField):
    def label(self):
        return "Training Exam"

    def default(self):
        return "General"

    def options(self):
        return [
            "General",
            "Pre",
            "Post"
        ]


class GenderField(RadioButtonsField):
    def label(self):
        return "Gender"

    def default(self):
        return "Male"

    def options(self):
        return [
            "Male",
            "Female"
        ]


class WeightGroupField(RadioButtonsField):
    def label(self):
        return "Weight Group"

    def default(self):
        return "M"

    def options(self):
        return [
            "M",
            "L",
            "XL"
        ]


class AgeField(TextboxField):
    def label(self):
        return "Age"

    def default(self):
        return "40"


class DataDurationField(TextboxField):
    def label(self):
        return "StaticData Duration"

    def default(self):
        return "60"


class NotesField(ScrollableTextboxField):
    def label(self):
        return "Notes"

    def default(self):
        return ""


