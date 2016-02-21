import csv
import itertools
import os

AMBIENT_TEMP = 20  # temperature (in C) of air outside of water heater
INLET_TEMP = 10  # temperature of water (in C) at inlet

class Environment(object):
    def __init__(self, mapping, start_hour=0):
        self._mapping = mapping
        self._current_hour = start_hour

    @property
    def current_tuple(self):
        return self._mapping[self._current_hour]

    @property
    def demand(self):
        return self.current_tuple[0]

    @property
    def ambient_temperature(self):
        return self.current_tuple[1]

    @property
    def inlet_temperature(self):
        return self.current_tuple[2]

    def advance_hour(self):
        self._current_hour += 1

    def info(self):
        return {
            'current_hour': self._current_hour,
            'demand': self._demand,
            'ambient_temperature': self._ambient_temperature,
            'inlet_temperature': self._inlet_temperature,
        }

    def __eq__(self, other_environment):
        return self.info() == other_environment.info()

_environment_singleton = None
def environment():
    """Return the environment used over the whole simulation."""
    return _environment_singleton

def setup_temperature_csv(csv_location):
    # normal csv_location is '../Data/AirTemperature.csv'
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)

    return [row['Celcius'] for row in reader]

def setup_demand(csv_location):
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)

    return [row['Litres/Hour'] for row in reader]

def setup_environment(csv_directory):
    ambient = setup_temperature_csv(os.path.join(csv_directory, 'AirTemperature.csv'))
    inlet = setup_temperature_csv(os.path.join(csv_directory, 'IncomingWaterUse.csv'))
    daily_demand = setup_demand(os.path.join(csv_directory, 'WaterUse.csv'))

    yearly_demand = itertools.repeat(daily_demand, 365)  # copy for every day

    # now we want a mapping of demand/ambient/inlet for every hour
    # [(demand for hour 0, ambient 0, inlet 0), (demand 1, ambient 1, inlet 1), ...]
    mapping = zip(yearly_demand, ambient, inlet)
    _environment_singleton = Environment(mapping)
    return _environment_singleton

def time_step_to_hour(time_step_index):  # TODO
    return None
