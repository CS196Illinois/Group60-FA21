from socket import socket, AF_INET, SOCK_STREAM

from Project.global_utils import async_function
from Project.networking.helpers import recv_all, send_all

NUMBER_OF_CLIENTS = 10


class Hub(object):
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server = socket(AF_INET, SOCK_STREAM)
        self._running = True
        self._pending = {}
        self._sessions = {}  # TODO: Store session threads

    def _init_server(self):
        self._server.bind((self._host, self._port))
        self._server.listen(NUMBER_OF_CLIENTS)

    @async_function
    def _handle_new_clients(self):
        while True:
            client, addr = self._server.accept()
            session_key = recv_all(client).decode("utf-8")
            if not self._verify_session_key(session_key):
                send_all(client, '0'.encode("utf-8"))
                self._disconnect(client)
                continue
            if session_key in self._pending.keys():
                self._init_session(client, self._pending[session_key])
                send_all(client, '1'.encode("utf-8"))
                send_all(self._pending[session_key], '1'.encode("utf-8"))
                del self._pending[session_key]
            else:
                self._pending[session_key] = client

    def _init_session(self, first: socket, second: socket):
        self._forward(first, second)
        self._forward(second, first)

    @async_function
    def _forward(self, from_client: socket, to_client: socket):
        while True:  # TODO: Add termination condition
            data = recv_all(from_client)
            send_all(to_client, data)

    @staticmethod
    def _disconnect(connection: socket):
        connection.shutdown(2)
        connection.close()

    @staticmethod
    def _verify_session_key(key: str):
        return True
        # TODO: Verify session keys

    def run(self):
        self._init_server()
        self._handle_new_clients()
