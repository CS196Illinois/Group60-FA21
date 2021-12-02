from time import sleep

import sys
sys.path.append("./")
from Project.networking.Events.event import Event
from Project.networking.hub import Hub
from Project.networking.secure_client import SecureClient

h = Hub('0.0.0.0', 8485)
c1 = SecureClient('127.0.0.1', 8485, "101")
c2 = SecureClient('127.0.0.1', 8485, "101")

h.run()
c1.connect()
c2.connect()
while not (c1.ready and c2.ready):
    sleep(0.1)

c1.send(Event())
print(c2.recv())

c1.change_key()
c2.recv()

c1.send(Event())
print(c2.recv())
