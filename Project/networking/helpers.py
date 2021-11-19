import struct
from socket import socket


def send_all(sock: socket, data: bytes):
    packed = struct.pack('>I', len(data)) + data
    sock.sendall(packed)


def recv_all(sock: socket):
    size = int(struct.unpack('>I', sock.recv(4))[0])
    if not size:
        return None

    data = bytearray()
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data.extend(packet)

    return data
