from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Image(QLabel):
    def __init__(self, *args):
        super(Image, self).__init__(*args)
        self.file_path = None
        self.pixmap: QPixmap = None

    def setSource(self, file_path):
        self.file_path = file_path
        self.pixmap = QPixmap(self.file_path)
        self.pixmap = self.pixmap.scaledToHeight(30)
        self.setPixmap(self.pixmap)

