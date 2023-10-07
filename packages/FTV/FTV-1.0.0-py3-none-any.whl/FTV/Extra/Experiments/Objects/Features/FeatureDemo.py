from FTV.Extra.Experiments import Feature
from FTV.Extra.Experiments import Dialog, Dialog2, Dialog3, Dialog4
from FTV.Extra.Experiments.Objects.Containers.MainWindow import MainWindow


class FeatureDemo(Feature):
    def init(self):
        txt_question = "Would you like to answer the question?"
        btn_yes = "Yes"
        btn_no = "No"
        Dialog.setItem(txt_question, btn_yes, btn_no)

        txt_question = "One more?"
        btn_yes = "Fine"
        btn_no = "Definitely no"
        Dialog2.setItem(txt_question, btn_yes, btn_no)

        txt_question = "Are you sure?"
        btn_yes = "I am"
        btn_no = "I am not"
        Dialog3.setItem(txt_question, btn_yes, btn_no)

        txt_question = "Would you like to answer the question?"
        btn_yes = "Yes"
        btn_no = "No"
        Dialog4.setItem(txt_question, btn_yes, btn_no)

        MainWindow.setCell(Dialog, "A")
        MainWindow.setCell(Dialog2, "B")
        MainWindow.setCell(Dialog3, "C")
        MainWindow.setCell(Dialog4, "D")

    # def setSettings(self):
    #     self.setUIPlatform(UIPlatforms.PyQt5)
