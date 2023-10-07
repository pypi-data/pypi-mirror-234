from PyQt5.QtWidgets import QComboBox

from Objects.UI.General import Widget


class Combobox(QComboBox, Widget):
    def __init__(self, *args):
        super(Combobox, self).__init__(*args)
        self.setTextSize(11)
        self.setMaxVisibleItems(20)

    # def addItems(self, texts: typing.Iterable[str]) -> None:
    #     super().addItems(texts)
    #     # self.setEditable(True)
    #     self.adjustSize()
