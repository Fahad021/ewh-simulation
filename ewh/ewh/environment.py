AMBIENT_TEMP = 20  # temperature (in C) of air outside of water heater
INLET_TEMP = 10  # temperature of water (in C) at inlet

class Environment(object):
    def __init__(self,
                 initial_ambient_temperature=AMBIENT_TEMP,
                 initial_inlet_temperature=INLET_TEMP):
        self._ambient_temperature = initial_ambient_temperature
        self._inlet_temperature = initial_inlet_temperature

    @property
    def ambient_temperature(self):
        return self._ambient_temperature

    @property
    def inlet_temperature(self):
        return self._inlet_temperature

    def update_environment(new_ambient=None, new_inlet=None):
        if new_ambient is not None:
            self._ambient_temperature = new_ambient

        if new_inlet is not None:
            self._inlet_temperature = new_inlet

    def info(self):
        return {
            'ambient_temperature': self._ambient_temperature,
            'inlet_temperature': self._inlet_temperature,
        }

    def __eq__(self, other_environment):
        return self.info() == other_environment.info()

_environment_singleton = None
def environment():
    """Return the environment used over the whole simulation."""
    if _environment_singleton is None:
        _environment_singleton = Environment(initial_ambient_temperature=AMBIENT_TEMP,
            initial_inlet_temperature=INLET_TEMP)
    return _environment_singleton
