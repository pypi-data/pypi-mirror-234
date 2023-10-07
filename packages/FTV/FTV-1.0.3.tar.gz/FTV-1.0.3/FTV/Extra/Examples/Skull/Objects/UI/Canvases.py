import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from Objects.UI.General import AppRunner

sys.path.append(str(Path(__file__).parents[2]))


class EnvCanvas(QWidget):
    def __init__(self, size):
        super(EnvCanvas, self).__init__()
        self.setFixedSize(size)
        self._createImage()

        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image,
                                self.image.rect())
        self.painter = QPainter(self.image)

    # paintEvent for creating blank canvas
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image,
                                self.image.rect())

    def setFixedSize(self, a0: QSize) -> None:
        super(EnvCanvas, self).setFixedSize(a0)
        self._createImage()

    def _createImage(self):
        # creating canvas
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def __enter__(self):
        self.painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        self.painter.setPen(QPen(Qt.transparent))
        self.painter.drawRect(self.image.rect())
        return self.painter

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            raise exc_value
        # updating it to canvas
        self.update()


if __name__ == "__main__":

    class Window(QMainWindow):
        def __init__(self):
            super().__init__()

            title = "Paint and save Application"

            top = 400
            left = 400
            width = 800
            height = 600

            # setting title of window
            self.setWindowTitle(title)

            # setting geometry
            self.setGeometry(top, left, width, height)

            # # creating canvas
            # self.canvas = EnvCanvas(self)

            self.canvas_parent = QWidget()
            self.canvas = EnvCanvas(QSize(720, 480))

            temp_lay = QVBoxLayout()
            temp_lay.addWidget(self.canvas)
            temp_lay.setContentsMargins(0, 0, 0, 0)

            self.canvas_parent.setLayout(temp_lay)
            self.canvas_layout = QVBoxLayout()
            self.canvas_layout.addWidget(self.canvas_parent)

            self.centralWidget = QWidget()
            self.centralWidget.setLayout(self.canvas_layout)

            self.setCentralWidget(self.centralWidget)
            self.setCentralWidget(self.canvas)

            # calling draw_something method
            self.draw_something()
            self.draw_something_2()

        # this method will draw a line
        def draw_something(self):
            # painter = QPainter(self.canvas.image)
            with self.canvas as painter:
                painter.setPen(QPen(Qt.black, 5, Qt.SolidLine,
                                    Qt.RoundCap, Qt.RoundJoin))
                # drawing a line
                painter.drawLine(100, 100, 300, 300)
            # self.canvas.update()

        def draw_something_2(self):
            # painter = QPainter(self.canvas.image)
            with self.canvas as painter:
                painter.setPen(QPen(Qt.transparent))
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

                # drawing a rectangle
                painter.drawRect(100, 200, 100, 100)
            # self.canvas.update()


    with AppRunner() as ar:
        window = Window()
        ar.setApp(window)
