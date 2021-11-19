from typing import Callable
from threading import Thread


def async_function(func: Callable):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper
