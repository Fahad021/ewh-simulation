import enum

class State(enum.Enum):
    def __str__(self):
        return self.name

class OnState(State):
    OFF = 0
    ON = 1

class PowerUsage(State):
    LOW = 0
    REGULAR = 1

class TankSize(State):
    SMALL = 180
    LARGE = 270
