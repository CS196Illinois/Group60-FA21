import logging
from time import sleep

from Project.networking.Events.frame_event import FrameEvent
from Project.networking.event_handler import EventHandler
from Project.networking.secure_client import SecureClient
from Project.networking.hub import Hub


logger = logging.getLogger(__name__)

h = Hub('0.0.0.0', 8485)

event_handler = EventHandler({FrameEvent: lambda a: print(a.id)})
c2 = SecureClient('127.0.0.1', 8485, "88888888", event_handler)

h.run()

c2.connect()

while not c2.connection_ready:
    sleep(0.1)
print("connection ready")
while not c2.ready:
    sleep(0.1)
print("ready")
c2.handle_events()
