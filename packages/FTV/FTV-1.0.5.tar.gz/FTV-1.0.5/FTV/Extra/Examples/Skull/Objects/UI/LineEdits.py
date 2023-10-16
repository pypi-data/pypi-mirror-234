from PyQt5.QtWidgets import QLineEdit

from Objects.UI.General import Widget


class LineEdit(QLineEdit, Widget):
    def __init__(self, *args):
        super(LineEdit, self).__init__(*args)
        self.setTextSize(11)
