from functools import singledispatchmethod
from typing import Dict


class EventHandler(object):
    def __init__(self, callbacks: Dict):
        for event_type, callback in callbacks:
            self.handle.register(type(event_type), lambda event: callback(event))

    @singledispatchmethod
    def handle(self, arg):
        raise ValueError(f"Unhandled type {type(arg)}")
