""" Logging adapter """

from abc import ABC, abstractmethod
import json, time

class AppLogger(ABC):
    @abstractmethod
    def log(self, level: str, message: str) -> None:
        pass

class LegacyLogger:
    def write(self, priority: int, msg: str):
        print(f"[Legacy]: {priority}] {msg}")

class JsonLogger:
    def emit(self, record: dict):
        print(json.dumps(record))

class LegacyAdapter(AppLogger):
    LEVELS = {
        "debug": 10,
        "info": 20,
        "warning": 30,
        "error": 40,
    }

    def __init__(self, lg: LegacyLogger):
        self.lg = lg

    def log(self, level: str, message: str) -> None:
        self.lg.write(self.LEVELS.get(level, 20), message)

class JsonAdapter(AppLogger):
    def __init__(self, jl: JsonLogger):
        self.jl = jl

    def log(self, level: str, message: str) -> None:
        self.jl.emit({"ts": time.time(), "level": level, "msg": message})

logger: AppLogger = LegacyAdapter(LegacyLogger())
logger.log("warn", "Disk Space Low")
logger = JsonAdapter(JsonLogger())
logger.log("info", "Service Started")

# The old logger expects an integer priority, the JSON Logger expects a dictionary.
# The adapters map the "log(level, message)" interface into the corresponding format.
# The Application code doesnt need to change whether you log to legacy systems or structured JSON