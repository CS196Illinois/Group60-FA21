import logging
import sys
from typing import Optional
from PyQt5 import QtWidgets, QtQml, QtCore, QtGui
#pip3 install PyQt5

logger = logging.getLogger(__name__)


class BaseApplication(object):
    def __init__(self, main_view: str, window_name: str = "Application"):
        self._app = None  # type: Optional[QtWidgets.QApplication]
        self._engine = None  # type: Optional[QtQml.QQmlApplicationEngine]
        self._window = None  # type: Optional[QtGui.QWindow]
        self._main_view = main_view
        self.window_name = window_name

    def _init_app(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._engine = QtQml.QQmlApplicationEngine()
        # noinspection PyUnresolvedReferences
        self._engine.quit.connect(self._shutdown)

    def _set_app_input(self):
        # context = self._engine.rootContext()
        # context.setContextProperty("someVM", self._some_view_model)
        pass

    def _create_window(self):
        self._engine.load(QtCore.QUrl().fromLocalFile(self._main_view))
        self._window = self._engine.rootObjects()[0]
        self._window.setTitle(self.window_name)

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
        self._run()
        self._run_app()

    def _run(self):
        self._init_exception_handler()
        self._init_app()
        self._set_app_input()
        self._create_window()
