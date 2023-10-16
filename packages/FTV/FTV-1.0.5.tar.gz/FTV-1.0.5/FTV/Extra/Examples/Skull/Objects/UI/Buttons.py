from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from FTV.Extra.Examples.Skull.Objects.UI import Widget, AppRunner


class Button(QPushButton, Widget):
    ICON_DIR = None

    def __init__(self, *args, icon=None, icon_dir=None):
        super(Button, self).__init__(*args)

        if icon_dir is None:
            self.icon_dir = self.__class__.ICON_DIR
        else:
            self.icon_dir = self.icon_dir

        self.icon = icon

        if self.icon is not None:
            self.icon_path = self.icon_dir + self.icon
        else:
            self.icon_path = None

        self.setIcon(QIcon(self.icon_path))
        self.setTextSize(11, 1)

    def setFixedIconSize(self, w, h):
        self.setIconSize(QSize(w, h))

    @classmethod
    def setIconDir(cls, icon_dir):
        cls.ICON_DIR = icon_dir


class ActionButton(Button):
    def __init__(self, *args, icon=None, icon_dir=None):
        super(ActionButton, self).__init__(*args, icon=icon, icon_dir=icon_dir)
        self.setFixedHeight(30)
        self.setTextSize(14, 2)


class TopMenuBarButton(Button):
    def __init__(self, icon=None, icon_dir=None):
        Button.__init__(self, icon=icon, icon_dir=icon_dir)

        self.setup()

    def setup(self):
        self.setFixedSize(50, 50)
        self.setFixedIconSize(30, 30)


if __name__ == '__main__':
    with AppRunner() as ar:
        b = TopMenuBarButton("play.png")
        b = TopMenuBarButton("pause.png")
        b = TopMenuBarButton("lightning.png")
        ar.setApp(b)
