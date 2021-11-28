import ctypes
from functools import wraps

from typing import Callable
from threading import Thread
from mss import mss

from Project.networking.Events.frame_event import FrameEvent


def async_function(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


def get_dimensions():
    user32 = ctypes.windll.user32
    return {'top': 0,
            'left': 0,
            'width': user32.GetSystemMetrics(0),
            'height': user32.GetSystemMetrics(1)}


def screenshot(rect: dict) -> FrameEvent:
    with mss() as sct:
        img = sct.grab(rect)
        return FrameEvent(img)
