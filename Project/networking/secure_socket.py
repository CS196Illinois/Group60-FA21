from socket import socket, AF_INET, SOCK_STREAM

from Project.networking.helpers import send_all, recv_all


class ConnectionNotReady(Exception):
    def __init__(self):
        super(ConnectionNotReady, self).__init__("Connection is not ready")


class SecureSocket(object):
    def __init__(self):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self.connection_ready = False
        # TODO: Implement encrypted socket connection

    def connect(self, host: str, port: int, session_key: str):
        self._socket.connect((host, port))
        send_all(self._socket, session_key.encode("utf-8"))
        response = int(recv_all(self._socket).decode("utf-8"))
        if response:
            self.connection_ready = True
        return self.connection_ready
        # TODO: Extend connect to implement encryption protocol

    def send(self, data: bytes):
        if not self.connection_ready:
            raise ConnectionNotReady()
        send_all(self._socket, data)

    def recv(self):
        return recv_all(self._socket)

