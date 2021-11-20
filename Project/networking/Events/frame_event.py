from mss.screenshot import ScreenShot

from Project.networking.Events.event import Event
from zlib import compress, decompress


class FrameEvent(Event):
    def __init__(self, shot: ScreenShot, compression=6):
        super(FrameEvent, self).__init__()
        self._pixels = compress(shot.rgb, compression)
        self.size = shot.size

    @property
    def pixels(self) -> bytes:
        return decompress(self._pixels)
