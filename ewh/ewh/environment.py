import csv
import itertools
import os
import pprint
import math

import config

class Environment(object):
    def __init__(self, mapping, time_scaling_factor, start_hour=0):
        self._mapping = mapping
        self._current_hour = start_hour
        self._tsf = time_scaling_factor
        self._current_timestep = start_hour

    @property
    def current_tuple(self):
        """(demand [L/h], ambient [deg C], inlet [deg C])"""
        return self._mapping[self._current_hour]

    @property
    def demand(self):
        """Water demand (in litres per hour)"""
        return self.current_tuple[0]

    @property
    def ambient_temperature(self):
        """Temperature (in degrees C) of area outside of the EWH population"""
        return self.current_tuple[1]

    @property
    def inlet_temperature(self):
        """Temperature (in degrees C) of inlet water"""
        return self.current_tuple[2]

    @property
    def time_scaling_factor(self):
        """Integer number of time steps that comprise exactly one hour"""
        return self._tsf

    @property
    def current_hour(self):
        """Current hour of the simulation, floored"""
        return self._current_hour

    @property
    def time_tuple(self):
        """(Current day, current hour of day, current minute of hour), zero-indexed"""
        minutes_since_hour_start = (self._current_timestep * (60/self._tsf)) - (self.current_hour * 60)
        return (math.floor(self._current_hour / 24), self._current_hour % 24, math.floor(minutes_since_hour_start))

    def is_at_non_peak_boundary(self):
        """Return True if environment is exactly at 10am or 8pm"""
        _, hours, minutes = self.time_tuple
        during_non_peak = hours in [10, 20]
        at_boundary = minutes < (60/self._tsf)
        return during_non_peak and at_boundary

    def is_at_peak_boundary(self):
        """Return True if environment is exactly at 6am or 4pm"""
        _, hours, minutes = self.time_tuple
        during_peak = hours in [6, 16]
        at_boundary = minutes < (60/self._tsf)
        return during_peak and at_boundary

    def is_in_reactivation_period(self):
        return self._current_hour in (10, 20)

    def is_at_quarter_hour_boundary(self):
        return self.time_tuple[2] in (0,15,30,45)

    def reactivation_zone(self):
        minutes = math.floor(self.time_tuple[2] / 15)
        return range(0,4).index(minutes)

    def sync_timestep(self, time_step_index):
        """Set the hour of the simulation according to the given time step"""
        self._current_timestep = time_step_index
        self._current_hour = math.floor(self._current_timestep / self._tsf)

    def info(self):
        return {
            'current_hour': self._current_hour,
            'demand': self.demand,
            'ambient_temperature': self.ambient_temperature,
            'inlet_temperature': self.inlet_temperature,
            'time_scaling_factor': self._tsf,
        }

_environment_singleton = None
def environment():
    """Return the environment used over the whole simulation."""
    return _environment_singleton

def setup_temperature_csv(csv_location):
    """Return a list of CSV values containing day & temperature data. The index
of the list represents the day of the year, and the value at that index represents
the temperature at that day.
    """
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [list(itertools.repeat(float(row['Celsius']), 24)) for row in reader]
    return rows

def setup_demand(csv_location):
    """Return a list of CSV values containing hour & temperature data. The index
of the list represents the hour of the day, and the value at that index represents
the demand (in L/h) at that hour.
"""
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [float(row['Litres/Hour']) for row in reader]
    return rows

def setup_environment(csv_directory, time_scaling_factor):
    """Build up an environment from the time/temperature/demand mappings in the
given CSV directory. The given TSF is also included.
"""
    ambient = setup_temperature_csv(os.path.join(csv_directory, 'AirTemperature.csv'))
    inlet = setup_temperature_csv(os.path.join(csv_directory, 'IncomingWaterTemperature.csv'))
    daily_demand = setup_demand(os.path.join(csv_directory, 'WaterUse.csv'))

    yearly_demand = list(itertools.repeat(daily_demand, 365))  # copy for every day
    # now we want a mapping of demand/ambient/inlet for every hour
    # [(demand for hour 0, ambient 0, inlet 0), (demand 1, ambient 1, inlet 1), ...]
    mapping = zipper(yearly_demand, ambient, inlet)
    _environment_singleton = Environment(mapping, time_scaling_factor)
    return _environment_singleton

def zipper(demand, ambient, inlet):
    """Make the mapping between demand/ambient/inlet temperatures."""
    mapping = []
    for day_index in range(365):
        daily_demand = demand[day_index]
        daily_ambient = ambient[day_index]
        daily_inlet = inlet[day_index]
        for hour_index in range(24):
            mapping.append([daily_demand[hour_index], daily_ambient[hour_index], daily_inlet[hour_index]])

    return mapping
