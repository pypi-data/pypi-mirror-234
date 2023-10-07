
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget)

from FTV.Extra.Experiments import Container


FONT = "Arial"
FONT_SIZE = 10


class MainWindow(Container):
    def __init__(self):
        super().__init__()
        # self.question_label = QLabel("Lahav")
        # self.left_layout.addWidget(self.question_label)

    @classmethod
    def setupUI(cls):

        cls._setID(QStackedWidget(), "A")
        cls._setID(QStackedWidget(), "B")
        cls._setID(QStackedWidget(), "C")
        cls._setID(QStackedWidget(), "D")

        cls.left_layout = QVBoxLayout()
        cls.left_layout.setContentsMargins(0,0,0,0)
        cls.left_layout.setSpacing(2)
        cls.left_layout.addWidget(cls.getCell("A"))
        cls.left_layout.addWidget(cls.getCell("B"))

        cls.left_widget = QWidget()
        cls.left_widget.setLayout(cls.left_layout)

        cls.layout = QHBoxLayout()
        cls.layout.addWidget(cls.left_widget)
        cls.layout.addWidget(cls.getCell("C"))
        cls.layout.addWidget(cls.getCell("D"))

    @classmethod
    def setItem(cls, question, yes, no):
        pass
        # cls.question_label.setText(question)
        # cls.btn_yes.setText(yes)
        # cls.btn_no.setText(no)

if __name__ == '__main__':
    MainWindow.showDemo()