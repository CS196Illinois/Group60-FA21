import pickle
from datetime import datetime
from uuid import uuid1


class Event(object):
    def __init__(self):
        self.timestamp = datetime.now()
        self.id = uuid1()

    def pickle(self):
        return pickle.dumps(self)

    def dispose(self):
        del self

    def __hash__(self):
        return self.id.__hash__()

