from PyQt5.QtWidgets import QGroupBox

from FTV.Extra.Examples.Skull.Objects.UI import Widget


class GroupBox(QGroupBox, Widget):
    def __init__(self, *args):
        super(GroupBox, self).__init__(*args)
        self.setTextSize(11, 1)
        self.setStyleSheet('QGroupBox {color: grey;}')
