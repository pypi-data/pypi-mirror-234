from PyQt5.QtWidgets import QRadioButton

from Objects.UI.General import Widget


class RadioButton(QRadioButton, Widget):
    def __init__(self, *args):
        super(RadioButton, self).__init__(*args)
        self.setTextSize(11)
