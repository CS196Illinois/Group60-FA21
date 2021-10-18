import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class Hub:
    def __init__(self, ip: str, port: int, packet_size=4096):
        self._ip = ip
        self._port = port
        self._server = socket(AF_INET, SOCK_STREAM)
        self._client_data = {}
        self._packet_size = packet_size

        self._server.bind((self._ip, self._port))
        print('Socket bind complete')

        self._server.listen(10)
        print('Socket now listening')

        self.run()

    def _handle_new_clients(self):
        while True:
            client, addr = self._server.accept()
            self._client_data[client] = b''
            self._communicate_with_client(client)
            print("Connected to client: %s" % client)

    def _communicate_with_client(self, client):
        Thread(target=self._handle_from_client, args=(client,)).start()
        Thread(target=self._handle_to_client, args=(client,)).start()

    def _handle_from_client(self, client: socket, delay=0):
        while True:
            data = client.recv(self._packet_size)
            time.sleep(delay)
            self._client_data[client] = data

    def _handle_to_client(self, client: socket):
        while True:
            client_data = self._client_data
            for c in list(client_data.keys()):
                if c is not client:
                    data = client_data[c]
                    client.send(data)

    def remove_client(self, client: socket):
        del self._client_data[client]

    @property
    def data(self) -> dict:
        return self._client_data

    @property
    def clients(self) -> list:
        return list(self._client_data.keys())

    def run(self):
        Thread(target=self._handle_new_clients).start()
