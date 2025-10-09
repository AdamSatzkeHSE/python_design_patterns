"""Decorator pattern
Adding logging and caching to a data provider at runtime
"""

from functools import lru_cache
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

class DB(DataSource):
    def get(self, key: str) -> str:
        return f"DB_VALUE_FOR{key}"
    
class LoggingDecorator(DataSource):
    def __init__(self, wrapper: DataSource):
        self.wrapper = wrapper
    
    def get(self, key:str) -> str:
        print("[LOG] fetching", key)
        return self.wrapper.get(key)
    
class CachingDecorator(DataSource):
    def __init__(self, wrapper: DataSource):
        self.wrapper = wrapper

    @lru_cache(maxsize=None)
    def _cached_get(self, key: str) -> str:
        return self.wrapper.get(key)
    
    def get(self, key:str):
        return self._cached_get(key)
    
if __name__ == "__main__":
    source = CachingDecorator(LoggingDecorator(DB()))
    print(source.get("k1"))
    print(source.get("k1"))