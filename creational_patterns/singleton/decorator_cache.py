""" Cache using a Singleton Decorator
"""
from threading import Lock

def singleton(cls):
    """ A decorator that turns a class into a singleton """
    _instances = {}
    lock: Lock = Lock()

    def get_instance(*args, **kwargs):
        with lock:
            if cls not in _instances:
                print(f"Creating a single instance of {cls.__name__}")
                _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance

@singleton
class Cache:
    def __init__(self):
        print("Initializing Cache...")
        self._data = {}

    def set(self, key, value):
        self._data[key] = value
        print(f"Cache SET: {key} = {value}")
    
    def get(self, key):
        value = self._data.get(key)
        print(f"Cache GET: {key} -> {value}")
        return value
    