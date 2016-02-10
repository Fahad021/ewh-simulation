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

_environment_singleton = None
def environment():
    if _environment_singleton is None:
        _environment_singleton = Environment(initial_ambient_temperature=AMBIENT_TEMP,
            initial_inlet_temperature=INLET_TEMP)
    return _environment_singleton


class Simulation(object):
    def __init__(self):
        self._environment = environment()
        self._hub =
        self._population = []

    def add_controllers_to_population(self, population):
        self._population.extend(population)

    def run(self, time_steps=None, subset_size=None):
        pass

    def run_time_step(self, population_subset):
        pass

    def poll_controller_bidirectional(self, controller):
        controller.poll()

        message = controller.info(include_ewh=True)

        # TODO: ... coming soon to a theatre near you
