from abc import abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QWidget, QTextEdit, QButtonGroup, \
    QVBoxLayout, QGridLayout, QFrame, QSizePolicy

from Objects.UI.CheckBoxes import CheckBox
from Objects.UI.Combobox import Combobox
from Objects.UI.General import Widget
from Objects.UI.GroupBox import GroupBox
from Objects.UI.Labels import Label
from Objects.UI.LineEdits import LineEdit
from Objects.UI.RadioButton import RadioButton


class Field:
    def __init__(self):
        super().__init__()
        self.minimum_width = None
        self.maximum_width = None
        self.minimum_height = None
        self.maximum_height = None
        self._critical = self.critical()
        self._default = self.default()

        self.setupVariables()

        self._label = Label()
        self.setLabelText(self.label())

        self.body = Widget()
        self.setupBody()

        if self.maximum_width is not None and "setMaximumWidth" in dir(self.body):
            self.body.setMaximumWidth(self.maximum_width)

        if self.minimum_height is not None and "setMinimumHeight" in dir(self.body):
            self.body.setMinimumHeight(self.minimum_height)

        if self.maximum_height is not None and "setMaximumHeight" in dir(self.body):
            self.body.setMaximumHeight(self.maximum_height)

    @abstractmethod
    def label(self):
        return ""

    @abstractmethod
    def default(self):
        return ""

    def critical(self):
        return False

    def build(self):
        self._setupBody()
        self._setupBodyWrap()
        self.setSignals()

        self.setValue(self._default)
        return self

    def setCritical(self, critical):
        self._critical = critical

    def setLabelText(self, label):
        self._label.setText(f"{label}:")

    def getLabelText(self):
        return self._label.text()

    def getLabel(self):
        return self._label

    def getBody(self):
        return self.body

    def getBodyWrap(self):
        return self.body_wrap

    def setupVariables(self):
        self.maximum_width = 100

    def _setupBody(self):
        pass
        # if isinstance(self.body, QWidget):
        #     self.body.setStyleSheet(f"{self.body.__class__.__name__}"
        #                             f"{{ border: 1px solid rgb(150,150,150); }}")

    def _setupBodyWrap(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(*[0]*4)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft)

        if isinstance(self.body, QWidget):
            layout.addWidget(self.body)
        else:
            layout.addLayout(self.body)

        self.body_wrap = QFrame()
        self.body_wrap.setObjectName("body_wrap")
        self.body_wrap.setContentsMargins(*[0]*4)
        self.body_wrap.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # self.body_wrap.stretch(layout)
        self.body_wrap.setLayout(layout)

    @abstractmethod
    def setupBody(self):
        pass

    @abstractmethod
    def setSignals(self):
        pass

    @abstractmethod
    def setValue(self, value: object):
        pass
        # if self.critical:
        #     self.updateBorderColor(value)

    @abstractmethod
    def getValue(self) -> object:
        pass

    def setEnabled(self, value=True):
        self.body.setEnabled(value)

    def setDisabled(self, value=True):
        self.body.setDisabled(value)

    def defaultBorder(self):
        """border_size, (R,G,B,A)"""
        return 1, (0, 0, 0, 0)

    def criticalBorder(self):
        """border_size, (R,G,B,A)"""
        return 1, (255, 0, 0, 255)

    def updateBorderColor(self, value, bad_values=None):
        if bad_values is None:
            bad_values = [""]

        if value in bad_values:
            border, color = self.criticalBorder()
        else:
            border, color = self.defaultBorder()

        color = f"rgba{color}"

        self.body_wrap.setStyleSheet("QFrame#body_wrap { border : " + str(border) + "px solid " + color + "; }")
        # self.body.setMaximumWidth(self.original_width - 2 * border)
        self.body.setBaseSize(self.original_width - 2 * border,
                              self.original_height - 2 * border)

    def setBorderChangeSignal(self, signal, bad_values=None):
        if self._critical:
            signal.connect(lambda: self.updateBorderColor(self.getValue(), bad_values=bad_values))

            self.original_width = self.body.width()
            self.original_height = self.body.height()

            self.updateBorderColor(self.getValue(), bad_values=bad_values)


class CheckboxField(Field):
    def setupBody(self):
        self.body = QCheckBox()

    def setSignals(self):
        self.setBorderChangeSignal(self.body.stateChanged, [False])

    def setValue(self, value: bool):
        super().setValue(value)
        self.body.setChecked(value)

    def getValue(self) -> bool:
        return self.body.isChecked()


class TextboxField(Field):

    # def setupVariables(self):
    #     self.maximum_width = 80

    def setupBody(self):
        self.body = LineEdit()
        self.changed = self.body.textChanged

    def setSignals(self):
        self.setBorderChangeSignal(self.body.textChanged)

    def setValue(self, value: str):
        super().setValue(value)
        self.body.setText(value)

    def getValue(self) -> str:
        return self.body.text()


class ScrollableTextboxField(Field):
    def setupVariables(self):
        self.maximum_width = None
        self.maximum_height = 80
        # self.minimum_height = 80

    def setupBody(self):
        self.body = QTextEdit()
        self.body.setLineWrapMode(QTextEdit.NoWrap)

    def setSignals(self):
        self.setBorderChangeSignal(self.body.textChanged)

    def setValue(self, value: str):
        super().setValue(value)
        self.body.setText(value)

    def getValue(self) -> str:
        return self.body.toPlainText()


class ComboboxField(Field):
    def __init__(self):
        super(ComboboxField, self).__init__()
        options = self.options()
        if options is not None:
            self.addValueOptions(options)

    @abstractmethod
    def options(self) -> list[str]:
        return None

    def setupBody(self):
        self.body = Combobox()
        self.changed = self.body.currentTextChanged

    def setSignals(self):
        self.setBorderChangeSignal(self.body.currentTextChanged)

    def setValue(self, value: str):
        super().setValue(value)
        self.body.setCurrentText(value)

    def getValue(self) -> str:
        return self.body.currentText()

    def addValueOption(self, option: str):
        self.body.addItem(option)

    def removeValueOption(self, option: str):
        self.body.clear()
        options = self.options()
        options.remove(option)

        self.body.addItems(options)

    def addValueOptions(self, options: list[str]):
        self.body.addItems(options)

    def setValueOptions(self, options: list[str]):
        self.body.clear()
        self.body.addItems(options)


class MultiComboboxField(Field):
    def __init__(self):
        self.selected_values = []
        self.selected_items = []
        self._options = self.options()
        self._max_columns = self.max_columns()
        self.combo_box: Combobox = None
        self.grid_layout: QGridLayout = None
        super(MultiComboboxField, self).__init__()

        self.combo_box.setMaximumWidth(self.maximum_width)

    def setupVariables(self):
        self.maximum_width = 100

    def build(self):
        self._setupBody()
        self._setupBodyWrap()
        self.setSignals()

        self.addValueOptions(self._options)
        self.setValue(self._default)
        return self

    def setupBody(self):
        self.combo_box = Combobox()
        self.combo_box.setFixedWidth(self.maximum_width)
        self.combo_box.currentTextChanged.connect(self.onSelection)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        self.combo_box_layout = QVBoxLayout()
        self.combo_box_layout.setContentsMargins(0,4,5,0)
        self.combo_box_layout.setAlignment(Qt.AlignTop)
        self.combo_box_layout.addWidget(self.combo_box)

        self.body = QHBoxLayout()
        self.body.setAlignment(Qt.AlignTop)
        self.body.addLayout(self.combo_box_layout)
        self.body.addLayout(self.grid_layout)

    def setSignals(self):
        self.setBorderChangeSignal(self.combo_box.currentTextChanged)

    def setValue(self, values: list):
        for value in values:
            self.onSelection(value)

    def getValue(self) -> str:
        return self.body.currentText()

    def addValueOptions(self, options: list[str]):
        self._options = options
        self.combo_box.addItems([""] + self._options)
        self.combo_box.setCurrentText("")

    def setMaxColumns(self, max_columns):
        self._max_columns = max_columns

    def onSelection(self, value):
        if not value:
            return

        checkbox = CheckBox(value)
        checkbox.setChecked(True)

        layout = QHBoxLayout()
        layout.setContentsMargins(*[5]*4)
        layout.addWidget(checkbox)

        item = GroupBox()
        item.setLayout(layout)

        checkbox.stateChanged.connect(lambda: self.onDisSelection(item, value))

        num = len(self.selected_values)

        self.selected_values.append(value)
        self.selected_items.append(item)
        self.grid_layout.addWidget(item, *self.indexToRowCol(num))

        self.updateCombobox()

    def onDisSelection(self, item, value):
        index = self.selected_items.index(item)

        self.grid_layout.removeWidget(item)
        item.deleteLater()

        for i in range(index + 1, len(self.selected_values)):
            temp_item = self.selected_items[i]
            self.grid_layout.removeWidget(temp_item)
            self.grid_layout.addWidget(temp_item, *self.indexToRowCol(i-1))

        self.selected_items.remove(item)
        self.selected_values.remove(value)
        self.updateCombobox()

    def indexToRowCol(self, index):
        if self._max_columns is None:
            row = 0
            col = index
        else:
            row = index // self._max_columns
            col = index % self._max_columns

        return row, col

    def updateCombobox(self):
        self.combo_box.clear()
        options = self._options.copy()
        [options.remove(val) for val in self.selected_values]

        if options:
            self.combo_box.addItems([""] + options)

        self.body.setAlignment(Qt.AlignTop)

    @abstractmethod
    def options(self):
        return []

    @abstractmethod
    def max_columns(self):
        return None


class RadioButtonsField(Field):
    def __init__(self):
        super(RadioButtonsField, self).__init__()
        self.radio_buttons = []
        self._direction = self.direction()  # "horizontal" or "vertical"

        options = self.options()
        if options is not None:
            self.options = options

    @abstractmethod
    def options(self):
        return []

    def direction(self):
        return "horizontal"

    # def setupVariables(self):
    #     self.maximum_width = 80

    def setupBody(self):
        self.button_group = QButtonGroup()
        self.body = QHBoxLayout()

    def setSignals(self):
        self.setBorderChangeSignal(self.button_group.buttonClicked)

    def setValue(self, value: str):
        super().setValue(value)
        self.button_group.buttons()[self.getIndex(value)].setChecked(True)

    def getValue(self) -> str:
        return self.button_group.checkedButton().text()

    def addValueOptions(self, options: list[str]):
        self.body.setSpacing(20)
        for option in options:
            radio_button = RadioButton(option)
            self.radio_buttons.append(radio_button)
            self.button_group.addButton(radio_button)
            self.body.addWidget(radio_button)

    def getIndex(self, value: str):
        return next((i for i in range(len(self.radio_buttons)) if self.radio_buttons[i].text() == value), None)

    def setDirection(self, direction: str):
        if direction == "horizontal":
            self.body = QHBoxLayout()
        elif direction == "vertical":
            self.body = QVBoxLayout()
        else:
            raise Exception(f"direction '{direction}' is not supported.")

        self.body.setAlignment(Qt.AlignLeft)

    def build(self):
        self._setupBody()
        self._setupBodyWrap()
        self.setSignals()

        self.addValueOptions(self.options)
        self.setValue(self._default)
        self.setDirection(self._direction)
        return self


class GroupField(Field):
    @abstractmethod
    def setupBody(self):
        pass

    @abstractmethod
    def setValue(self, value: str):
        super().setValue(value)

    @abstractmethod
    def getValue(self) -> object:
        pass

    # @abstractmethod
    # def addSubField(self, label, value, check_default):
    #     pass

    @abstractmethod
    def _addSubFields(self, sub_fields):
        pass

    @abstractmethod
    def subFields(self):
        return []


class TextboxGroupField(GroupField):
    def __init__(self):
        super(TextboxGroupField, self).__init__()
        self.body_sub_layouts = []

    def setupBody(self):
        self.body = QHBoxLayout()
        self.body_sub_layouts = []

    def setValue(self, value: str):
        super().setValue(value)

    def getValue(self) -> object:
        pass

    def addSubField(self, text, value):
        text_edit = LineEdit(value)
        text_edit.setMaximumWidth(40)
        label = Label(f"{text}:")

        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.LeftToRight)
        layout.setContentsMargins(*[5]*4)
        layout.addWidget(label)
        layout.addWidget(text_edit)
        layout.setAlignment(text_edit, Qt.AlignLeft)

        group_box = GroupBox()
        group_box.setLayout(layout)

        self.body_sub_layouts.append(layout)
        self.body.addWidget(group_box)

    def _addSubFields(self, sub_fields):
        self.body.setSpacing(15)
        for sub_field in sub_fields:
            sub_field = sub_field()
            self.addSubField(sub_field.label(), sub_field.default())

    def setDirection(self, direction: str):
        if direction == "horizontal":
            self.body = QHBoxLayout()
        elif direction == "vertical":
            self.body = QVBoxLayout()
        else:
            raise Exception(f"direction '{direction}' is not supported.")

        self.body.setAlignment(Qt.AlignLeft)

    def build(self):
        super().build()
        self._addSubFields(self.subFields())
        return self


class CheckboxTextboxGroupField(GroupField):
    def __init__(self):
        super(CheckboxTextboxGroupField, self).__init__()
        self.checkboxes = []

    def setupBody(self):
        self.body = QHBoxLayout()
        self.checkboxes = []

    def setValue(self, value: str):
        super().setValue(value)

    def getValue(self) -> object:
        pass

    def addSubField(self, text, value, check_default):
        checkbox = QCheckBox()
        checkbox.setChecked(check_default)

        text_edit = LineEdit(value)
        text_edit.setMaximumWidth(40)

        label = Label(f"{text}:")

        checkbox.stateChanged.connect(lambda: self.updateEnableField(checkbox, text_edit, label))

        layout = QHBoxLayout()
        layout.setContentsMargins(*[5]*4)
        layout.setDirection(QHBoxLayout.LeftToRight)
        layout.setSpacing(10)
        layout.addWidget(checkbox)
        layout.addWidget(label)
        layout.addWidget(text_edit)
        layout.setAlignment(text_edit, Qt.AlignLeft)

        group_box = GroupBox()
        group_box.setLayout(layout)

        self.checkboxes.append(checkbox)
        self.body.addWidget(group_box)
        self.updateEnableField(checkbox, text_edit, label)

    def _addSubFields(self, sub_fields):
        self.body.setSpacing(15)
        for sub_field, check_default in sub_fields:
            sub_field = sub_field()
            self.addSubField(sub_field.label(), sub_field.default(), check_default)

    def setDirection(self, direction: str):
        if direction == "horizontal":
            self.body = QHBoxLayout()
        elif direction == "vertical":
            self.body = QVBoxLayout()
        else:
            raise Exception(f"direction '{direction}' is not supported.")

        self.body.setAlignment(Qt.AlignLeft)

    def updateEnableField(self, checkbox, text_edit, label):
        enabled = checkbox.isChecked()
        text_edit.setEnabled(enabled)
        label.setEnabled(enabled)

        number_of_checked = len([item for item in self.checkboxes if item.isChecked()])

        if number_of_checked + 1 == len(self.checkboxes):
            [item.setEnabled(False) for item in self.checkboxes if not item.isChecked()]
        else:
            [item.setEnabled(True) for item in self.checkboxes]

    def build(self):
        super().build()
        self._addSubFields(self.subFields())
        return self


class SubField:
    @abstractmethod
    def label(self):
        return ""

    @abstractmethod
    def default(self):
        return ""


class SubTextboxField(SubField):
    @abstractmethod
    def label(self):
        return ""

    @abstractmethod
    def default(self):
        return ""
