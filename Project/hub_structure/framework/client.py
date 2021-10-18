from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

HEADER_SIZE = 10


class Client:
    def __init__(self, host: str, port: int, client_id: int, packet_size=4096):
        self._host = host
        self._port = port
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._data = b''
        self._packet_size = packet_size
        self._client_id = client_id

        self._received_data = {}
        self._temp_frames = [b'']

        self.run()

        self._socket.connect((self._host, self._port))
        print("Connected to server")

        Thread(target=self._listen_to_server).start()

    def _broadcast(self, callback, exit_func):
        while exit_func:
            data = callback()
            self.send(data)

    def _update_data(self):
        while True:
            try:
                sender_id, data = self._unpack(self.get_data())
                self._received_data[sender_id] = data
            except ValueError:
                pass

    def run(self):
        Thread(target=self._update_data).start()

    @staticmethod
    def _pack(unique_id, data):
        header = bytes(f"{unique_id:<{HEADER_SIZE}}", "UTF-8")
        return header + data

    @staticmethod
    def _unpack(msg) -> (int, bytes):
        sender_id = int(msg[:HEADER_SIZE].strip())
        data = msg[HEADER_SIZE:]
        return sender_id, data

    def _listen_to_server(self):
        while True:
            data = self._socket.recv(self._packet_size)
            self._data = data

    def get_data(self) -> bytes:
        return self._data

    @property
    def clients_data(self):
        return self._received_data

    def send(self, data):
        self._socket.send(self._pack(self._client_id, data))

    def broadcast(self, callback, exit_func=lambda: True):
        Thread(target=self._broadcast, args=(callback, exit_func)).start()
