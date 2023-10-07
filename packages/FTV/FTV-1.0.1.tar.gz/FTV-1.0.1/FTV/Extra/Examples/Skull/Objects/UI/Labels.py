from PyQt5.QtWidgets import QLabel

from FTV.Extra.Examples.Skull.Objects.UI import Widget


class Label(QLabel, Widget):
    def __init__(self, *args):
        super(Label, self).__init__(*args)
        self.setTextSize(11)
