from time import sleep
from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtProperty, pyqtSignal

from Project.global_utils import async_function, screenshot, get_dimensions
from Project.networking.Events.frame_event import FrameEvent
from Project.networking.secure_client import SecureClient

HOST_IP = '127.0.0.1'
HOST_PORT = 8485


class SharingViewModel(QtCore.QObject):
    stateChanged = pyqtSignal(int)

    def __init__(self):
        super(SharingViewModel, self).__init__()
        self._client = None  # type: Optional[SecureClient]
        self._sharing_screen = False
        self._state = 0

    # noinspection PyPep8Naming
    @pyqtSlot(str)
    def launchClient(self, key: str):
        if not self._client:
            self._client = SecureClient(HOST_IP, HOST_PORT, key)
            self._update_state()
            self._client.connect()

    def _launch_screen_sharing(self):
        dimensions_rect = get_dimensions()
        if self._client and not self._sharing_screen:
            self._sharing_screen = True
            self._client.broadcast(lambda: screenshot(dimensions_rect))

    # noinspection PyPep8Naming
    @pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self._state

    @state.setter
    def state(self, state: int):
        self._state = state
        self.stateChanged.emit(state)

    @async_function
    def _update_state(self):
        while not self._client.connection_ready:
            sleep(0.2)
        self.state = 1
        while not self._client.ready:
            sleep(0.2)
        self.state = 2
        self._launch_screen_sharing()
        while not self._sharing_screen:
            sleep(0.2)
        self.state = 3
        self._client.handle_broadcasts()






