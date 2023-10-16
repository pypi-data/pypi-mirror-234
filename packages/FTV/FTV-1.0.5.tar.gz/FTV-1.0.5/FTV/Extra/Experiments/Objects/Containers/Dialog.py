from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget

from FTV.Extra.Experiments import Container


FONT = "Arial"
FONT_SIZE = 10

class Dialog(Container):
    txt_question = None
    txt_yes = None
    txt_no = None

    question_label: QLabel = None
    btn_yes: QPushButton = None
    btn_no: QPushButton = None

    @classmethod
    def setupUI(cls):

        cls.question_label = QLabel(cls.txt_question)
        cls.question_label.setFont(QFont(FONT, FONT_SIZE))

        cls.top_lay = QVBoxLayout()
        cls.top_lay.addWidget(cls.question_label)

        cls.btn_yes = QPushButton(cls.txt_yes)
        cls.btn_yes.setFont(QFont(FONT, FONT_SIZE))
        cls.btn_no = QPushButton(cls.txt_no)
        cls.btn_no.setFont(QFont(FONT, FONT_SIZE))

        cls.bottom_lay = QHBoxLayout()
        cls.bottom_lay.addWidget(cls.btn_yes)
        cls.bottom_lay.addWidget(cls.btn_no)

        cls.sub_layout = QVBoxLayout()
        cls.sub_layout.addLayout(cls.top_lay)
        cls.sub_layout.addLayout(cls.bottom_lay)

        cls.widget = QWidget()
        cls.widget.setLayout(cls.sub_layout)
        cls.widget.setContentsMargins(10,10,10,10)

        cls.layout = QVBoxLayout()
        cls.layout.addWidget(cls.widget)
        # return layout

    @classmethod
    def setItem(cls, question, yes, no):
        cls.question_label.setText(question)
        cls.btn_yes.setText(yes)
        cls.btn_no.setText(no)

class Dialog2(Dialog):
    pass

class Dialog3(Dialog):
    pass

class Dialog4(Dialog):
    pass

if __name__ == '__main__':
    Dialog.showDemo()