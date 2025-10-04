""" A metaclass in Python defines how classes themselves behave
'a class of a class'

By customizing a metaclass, you can control how many times a class is instantiated.
"""

class SingletonMeta(type):
    _instances = {}
    """ Metaclass that creates a singleton base type
    when called"""
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"Creating instance of {cls.__name__}")
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# Implementation with a config manager
class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        print("Loading configuration...")
        self.settings = {
            "db_host" : "localhost",
            "db_port" : 3306,
            "debug" : True,
        }

    def get(self, key):
        return self.settings.get(key)
    
# Test
if __name__ == "__main__":
    config_1 = ConfigManager()
    config_2 = ConfigManager()

    print(config_1 is config_2)
    print(config_1.get("db_host"))
