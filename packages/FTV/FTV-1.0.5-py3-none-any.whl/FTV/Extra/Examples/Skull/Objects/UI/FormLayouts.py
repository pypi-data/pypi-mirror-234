from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFormLayout


class FormLayout(QFormLayout):
    def __init__(self, *fields_cls):
        super(FormLayout, self).__init__()
        self.state: list = None
        self.fields_cls = list(fields_cls)
        self.fields = []

        self.setupFields()
        self._setupForm()
        self.setSpacing(10)

    def setupFields(self):
        self.fields = []
        for field_cls in self.fields_cls:
            field = field_cls()
            field.build()
            self.fields.append(field)

    def _setupForm(self):
        for field in self.fields:
            self.addRow(field.getLabel(), field.getBodyWrap())

        if len(self.fields) >= 2:
            self.setAlignment(self.fields[-2].getBodyWrap(), Qt.AlignTop)

    # def saveState(self):
    #     return Json.write(self.state_file_path, self.state)

    def addField(self, field):
        self.fields.append(field)

    def getCriticalFields(self):
        return [item for item in self.fields if item.critical()]

    def areCriticalFieldsFull(self):
        return all(item.getValue() != "" for item in self.getCriticalFields())


class PatientFormLayout(FormLayout):
    pass


class ExaminationFormLayout(FormLayout):
    pass


# if __name__ == '__main__':
#     with AppRunner() as ar:
#         app = QWidget()
#         fieldManager = FormLayout(DATA_DIR + "examination_fields.json", DATA_DIR + "examination_fields_state.json")
#         app.setLayout(fieldManager)
#         ar.setApp(app)
