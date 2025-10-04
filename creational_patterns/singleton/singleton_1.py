""" The singleton pattern ensueres that a class has only one instance,
and provide a global point of access to that instance."""

""" Real use cases 
- Logging Systems
- Database Connections
- Configuration managers
- Thread pools
- Caches
"""


# Example: Logger 
import os
# Classic singleton with __new__
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating Logger instance")
            cls._instance = super().__new__(cls)
            cls._instance.log_file = os.path.join(os.path.dirname(__file__), "singleton.log")
        return cls._instance
    
    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + '\n')
        print(f"[LOGGED]: {message}")

# Test:
logger_1 = Logger()
logger_2 = Logger()

print(logger_1 is logger_2)

logger_1.log("Singleton test. This comes from the first object.")
logger_2.log("This comes from the 2nd object.")
