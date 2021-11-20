import logging

import mss

from Project.global_utils import screenshot, get_dimensions
from Project.networking.Events.event import Event
from Project.networking.twin_client import TwinClient
from Project.networking.hub import Hub


logger = logging.getLogger(__name__)

h = Hub('0.0.0.0', 8485)
c1 = TwinClient('127.0.0.1', 8485, "101")
c2 = TwinClient('127.0.0.1', 8485, "101")

h.run()
c1.connect()
c2.connect()
c1.send(screenshot(get_dimensions()))
frame = c2.recv()
mss.tools.to_png(frame.pixels, frame.size, output="output.png")
print("finished")
