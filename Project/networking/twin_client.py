import logging
import pickle
from socket import socket, AF_INET, SOCK_STREAM
from typing import Callable

from Project.global_utils import async_function
from Project.networking.Events.event import Event
from Project.networking.event_handler import EventHandler
from Project.networking.helpers import send_all, recv_all

logger = logging.getLogger(__name__)


class TwinClient(object):
    def __init__(self, host: str, port: int, session_key: str, event_handler: EventHandler = None):
        self._host = host
        self._port = port
        self._session_key = session_key
        self._event_handler = event_handler
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._broadcasted_callbacks = set()
        self._connection_ready = False
        self.running = False

    @property
    def ready(self):
        return self._connection_ready

    def send(self, event: Event):
        if not self.ready:
            logger.warning(f"Connection not ready")
            return
        send_all(self._socket, event.pickle())

    def recv(self) -> Event:
        return pickle.loads(recv_all(self._socket))

    def broadcast(self, callback: Callable):
        self._broadcasted_callbacks.add(callback)

    def terminate(self, callback: Callable):
        self._broadcasted_callbacks.remove(callback)

    def clear_broadcasts(self):
        self._broadcasted_callbacks.clear()

    @async_function
    def connect(self):
        try:
            self._socket.connect((self._host, self._port))
        except ConnectionRefusedError:
            logger.warning(f"Cannot connect to {self._host}:{self._port}")
            return False
        send_all(self._socket, self._session_key.encode("utf-8"))
        response = int(recv_all(self._socket).decode("utf-8"))
        if response:
            self._connection_ready = True
        else:
            logger.warning(f"Connection denied by server {self._host}:{self._port}")

        return self._connection_ready

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
