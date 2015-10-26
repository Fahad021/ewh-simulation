import enum

class State(enum):
    OFF = 0
    ON = 1

class Mode(enum):
    OFF = 0
    ON_NOT_READY = 1
    ON_READY = 2

class PowerUsage(enum):
    LOW = 0
    REGULAR = 1
