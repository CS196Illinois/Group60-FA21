import logging
import pickle
from typing import Callable, Type

from Project.global_utils import async_function
from Project.networking.Events.event import Event
from Project.networking.event_handler import EventHandler
from Project.networking.secure_socket import SecureSocket, ConnectionNotReady

logger = logging.getLogger(__name__)


class TwinClient(object):
    def __init__(self, host: str, port: int, session_key: str, event_handler: EventHandler = None):
        self._host = host
        self._port = port
        self._session_key = session_key
        self._event_handler = event_handler
        self._socket = SecureSocket()
        self._broadcasted_callbacks = set()
        self.running = False

    def send(self, event: Event):
        try:
            self._socket.send(event.pickle())
        except (TimeoutError, OSError, ConnectionNotReady) as exception:
            logger.warning(f"Send failed: {exception}")

    def recv(self):  # TODO: Add type
        return pickle.loads(self._socket.recv())

    def broadcast(self, callback: Callable):
        self._broadcasted_callbacks.add(callback)

    def terminate(self, callback: Callable):
        self._broadcasted_callbacks.remove(callback)

    def clear_broadcasts(self):
        self._broadcasted_callbacks.clear()

    @async_function
    def connect(self):
        if not self._socket.connect(self._host, self._port, self._session_key):
            logger.warning(f"Connection denied by server {self._host}:{self._port}")

    @async_function
    def _handle_broadcasts(self):
        while self.running:
            for callback in self._broadcasted_callbacks:
                event = callback()
                if not isinstance(event, Event):
                    logger.warning(f"Callback {callback} does not produce an event")
                    continue
                self.send(event)

    def _handle_events(self):
        while self._event_handler and self.running:
            event = self.recv()
            if not isinstance(event, Event):
                logger.warning(f"Expected event received {type(event)} instead")
                continue
            try:
                self._event_handler.handle(event)
            except ValueError as exception:
                logger.warning(exception)
