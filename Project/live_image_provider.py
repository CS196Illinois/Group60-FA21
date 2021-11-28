from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtQuick import QQuickImageProvider

from Project.global_utils import screenshot, get_dimensions


class LiveImageProvider(QQuickImageProvider):
    def __init__(self):
        super(LiveImageProvider, self).__init__(QQuickImageProvider.Pixmap)

    # def requestPixmap(self, p_str, size):
    #     rect = get_dimensions()
    #     frame = screenshot(rect)
    #     pixmap = QPixmap(frame.size.width, frame.size.height)
    #     pixmap.loadFromData(frame.pixels)
    #     return pixmap, pixmap.size()

    def requestPixmap(self, p_str, size):
        rect = get_dimensions()
        frame = screenshot(rect)
        print(len(frame.pixels))
        pixmap = QPixmap(frame.size.width, frame.size.height)
        pixmap.loadFromData(frame.pixels)
        print(pixmap, pixmap.size())
        return pixmap, pixmap.size()
