""" A cache stores temporary data to make repeated lookups faster.

You want to use only one cache instance shared across your app.
Otherwise, different modules might have inconsistent or duplicate data.

The singleton pattern ensures there's only one shared cache object.
"""

# Metaclass version
class SingletonMeta(type):
    """ Thread safe singleton metaclass. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If instance does not exist, create one.
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]

class Cache(metaclass=SingletonMeta):
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
    
    def clear(self):
        self._data.clear()
        print("Cache cleared.")

# Test
if __name__ == '__main__':
    cache_1 = Cache()
    cache_2 = Cache()

    print(cache_1 is cache_2)

    cache_1.set("MaxMustermann123", {"name" : "Max Mustermann", "age" : 30})
    cache_2.get("MaxMustermann123")