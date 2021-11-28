import logging
import sys
from typing import Optional
from PyQt5 import QtWidgets, QtQml, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtWidgets import QLabel

from Project.global_utils import screenshot, get_dimensions
from Project.gui.base_app import BaseApplication
from Project.remote_app.live_image import LiveImage
from Project.remote_app.view_models.remote_view_model import RemoteViewModel
from Project.live_image_provider import LiveImageProvider

logger = logging.getLogger(__name__)


class RemoteApplication(BaseApplication):
    QML_FILE = r'views\MainView.qml'

    def __init__(self):
        super(RemoteApplication, self).__init__(self.QML_FILE, "Remote Application")

        self._remote_view_model = RemoteViewModel()  # type: Optional[RemoteViewModel]


    def _set_app_input(self):
        context = self._engine.rootContext()
        context.setContextProperty("remoteVM", self._remote_view_model)
        self._engine.addImageProvider("myprovider", LiveImageProvider())

    def _set_image(self):
        print(self._window.children())
        rect = get_dimensions()
        data = screenshot(rect).pixels
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        live_image = self._window.findChild(QObject, "liveImage")
        # noinspection PyUnresolvedReferences
        live_image.setPixMap(pixmap)



if __name__ == "__main__":
    app = RemoteApplication()
    app.run()
