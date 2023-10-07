from PyQt5.QtWidgets import QTabWidget, QLayout, QWidget

from Objects.UI.General import Widget


class Tabs(QTabWidget, Widget):
    def __init__(self, *args):
        super(Tabs, self).__init__(*args)
        self.setTextSize(11)

    def addTab(self, layout: QLayout, name):
        widget = QWidget()
        widget.setLayout(layout)
        super(Tabs, self).addTab(widget, name)
