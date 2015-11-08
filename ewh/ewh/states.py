import enum

class OnState(enum.Enum):
    OFF = 0
    TOP = 1
    BOTTOM = 2

    def __str__(self):
        return self.name

class PowerUsage(enum.Enum):
    LOW = 0
    REGULAR = 1

    def __str__(self):
        return self.name
