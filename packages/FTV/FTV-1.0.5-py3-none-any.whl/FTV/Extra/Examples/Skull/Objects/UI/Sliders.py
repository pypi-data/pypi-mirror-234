from PyQt5.QtWidgets import QSlider

from Objects.UI.General import Widget


class Slider(QSlider, Widget):
    def __init__(self, *args):
        super().__init__(*args)
        self.setTextSize(11, 1)
