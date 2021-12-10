from typing import Dict


class EventHandler(object):
    def __init__(self, callbacks: Dict):
        self._callbacks = {event_type.__name__: lambda event: callback(event)
                           for event_type, callback in callbacks.items()}

    def handle(self, arg: object):
        self._callbacks[arg.__class__.__name__](arg)

    def add_handle(self, event_type, callback):
        self._callbacks[event_type.__name__] = lambda event: callback(event)
