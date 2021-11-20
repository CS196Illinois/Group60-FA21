from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class LiveImage(QLabel):
    def __init__(self):
        super(LiveImage, self).__init__()
        self._pixmap = QPixmap()

    # noinspection PyPep8Naming
    def updateImage(self, pixels: bytes) -> None:
        self._pixmap.loadFromData(pixels)
        self.setPixmap(self._pixmap)
        self.update()
