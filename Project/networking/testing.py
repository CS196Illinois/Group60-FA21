import time

from Project.networking.Events.event import Event
from Project.networking.twin_client import TwinClient
from Project.networking.hub import Hub

h = Hub('0.0.0.0', 8485)
c1 = TwinClient('127.0.0.1', 8485, "101")
c2 = TwinClient('127.0.0.1', 8485, "101")

h.run()
c1.connect()
c2.connect()
c1.send(Event())
print(c2.recv())