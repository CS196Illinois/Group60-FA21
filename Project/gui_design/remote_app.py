import logging
import sys
from typing import Optional
from PyQt5 import QtWidgets, QtQml, QtCore, QtGui

from Project.gui_design.view_models.remote_view_model import RemoteViewModel

logger = logging.getLogger(__name__)


class RemoteApplication(object):
    QML_FILE = r'views\MainView.qml'

    def __init__(self):
        self._app = None  # type: Optional[QtWidgets.QApplication]
        self._engine = None  # type: Optional[QtQml.QQmlApplicationEngine]
        self._window = None  # type: Optional[QtGui.QWindow]

        self._remote_view_model = None  # type: Optional[RemoteViewModel]

    def _init_app(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._engine = QtQml.QQmlApplicationEngine()
        # noinspection PyUnresolvedReferences
        self._engine.quit.connect(self._shutdown)

    def _init_view_models(self):
        self._remote_view_model = RemoteViewModel()

    def _set_app_input(self):
        context = self._engine.rootContext()
        context.setContextProperty("remoteVM", self._remote_view_model)

    def _create_window(self):
        self._engine.load(QtCore.QUrl().fromLocalFile(self.QML_FILE))
        self._window = self._engine.rootObjects()[0]
        self._window.setTitle("Sample Application")

    def _run_app(self):
        self._window.show()
        self._app.exec_()

    def _shutdown(self):
        if self._app is not None:
            self._app.quit()

    def _init_exception_handler(self):
        QtCore.qInstallMessageHandler(self._qt_message_handler)

    @staticmethod
    def _qt_message_handler(mode, context, message):
        # noinspection PyUnresolvedReferences
        if mode == QtCore.QtInfoMsg:
            mode = 'Info'
        elif mode == QtCore.QtWarningMsg:
            mode = 'Warning'
        elif mode == QtCore.QtCriticalMsg:
            mode = 'Critical'
        elif mode == QtCore.QtFatalMsg:
            mode = 'Fatal'
        else:
            mode = 'Debug'

        logger.warning("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))

    def run(self):
        self._init_exception_handler()
        self._init_app()
        self._init_view_models()
        self._set_app_input()
        self._create_window()
        self._run_app()


if __name__ == "__main__":
    app = RemoteApplication()
    app.run()
