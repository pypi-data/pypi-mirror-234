from PyQt5.QtWidgets import QCheckBox

from Objects.UI.General import Widget


class CheckBox(QCheckBox, Widget):
    def __init__(self, *args):
        super(CheckBox, self).__init__(*args)
        self.setTextSize(11)
