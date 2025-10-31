class Singleton(type):
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
    
class Config(metaclass=Singleton):
    def __init__(self):
        self._data = {}

    def set(self, k, v):
        self._data[k] = v
    
    def get(self, k, default=None):
        return self._data.get(k, default)
    
if __name__ == "__main__":
    c1 = Config()
    c2 = Config()

    c1.set("env", "prod")
    print("env from c2:", c2.get("env"))