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
        """Current hour of the simulation, unfloored"""
        return self._current_hour

    @property
    def time_tuple(self):
        """(Current day, current hour of day), zero-indexed"""
        return (math.floor(self._current_hour / 24), self._current_hour % 24)

    def is_in_peak_period(self):
        """Return True if environment is between hours of 6am-10am or 4pm-8pm"""
        hour_of_day = self.time_tuple[1]
        return hour_of_day in range(5, 9) or hour_of_day in range(13, 19)

    def is_in_immediate_non_peak_period(self):
        """Return True if environment is at 10am or 8pm"""
        hour_of_day = self.time_tuple[1]
        return hour_of_day in [9, 19]

    def sync_timestep(self, time_step_index):
        """Set the hour of the simulation according to the given time step"""
        self._current_hour = math.floor(time_step_index / self._tsf)

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
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [list(itertools.repeat(float(row['Celsius']), 24)) for row in reader]
    return rows

def setup_demand(csv_location):
    with open(csv_location) as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [float(row['Litres/Hour']) for row in reader]
    return rows

def setup_environment(csv_directory, time_scaling_factor):
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
    mapping = []
    for day_index in range(365):
        daily_demand = demand[day_index]
        daily_ambient = ambient[day_index]
        daily_inlet = inlet[day_index]
        for hour_index in range(24):
            mapping.append([daily_demand[hour_index], daily_ambient[hour_index], daily_inlet[hour_index]])

    return mapping
