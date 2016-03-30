from states import OnState, TankSize
import config
import environment

import time
import math
import logging
import pprint
import random

class ElectricWaterHeater(object):
    def __init__(self, randomize=False, state=OnState.OFF, configuration=None, env=None, hid=None):
        self._on_state = state

        if configuration is None:
            configuration = config.HeaterConfiguration()  # use default
        if env is None:
            env = environment.environment()

        self._config = configuration
        self._environment = env
        self._hid = hid

        self._current_demand = self._environment.demand
        self._lower_limit = self.configuration.regular_power_temperature
        self._upper_limit = self.configuration.desired_temperature

        if randomize:
            # set temperature somewhere within deadband
            self._temperature = random.uniform(self.configuration.regular_power_temperature, self.configuration.desired_temperature)
        else:
            # set to desired temperature
            self._temperature = self.configuration.desired_temperature

    @property
    def configuration(self):
        return self._config

    def go_to_low_power_mode(self):
        self._lower_limit = self.configuration.low_power_temperature
        self._upper_limit = self.configuration.regular_power_temperature

    def go_to_regular_power_mode(self):
        self._lower_limit = self.configuration.regular_power_temperature
        self._upper_limit = self.configuration.desired_temperature

    def heater_needs_to_turn_off(self):
        return (self._on_state == OnState.ON) and (self._temperature >= self._upper_limit)

    def heater_needs_to_turn_on(self):
        return (self._on_state == OnState.OFF) and (self._temperature < self._lower_limit)

    def heater_is_on(self):
        return self._on_state == OnState.ON

    def new_temperature(self, last_temperature):
        # G = surface area / thermal resistance of tank insulation
        g = self.configuration.tank_surface_area / self.configuration.insulation_thermal_resistance
        # B(t) = demand * 8.3 * (specific heat of water)
        b = to_gallons(self._current_demand) * 8.3 * config.SPECIFIC_HEAT_OF_WATER
        # C = equivalent thermal mass of tank
        # C = 8.3 * (number of gallons) * (specific heat of water)
        c = 8.3 * self.configuration.tank_gallons * config.SPECIFIC_HEAT_OF_WATER
        r_prime = 1.0 / (g + b)
        # scalar = e^((-1/R'C)(t - tau)) = e^(-1/R'C(TSF))
        scalar = math.exp(-1/(r_prime * c * self._environment.time_scaling_factor))

        ambient = to_fahrenheit(self._environment.ambient_temperature)
        inlet = to_fahrenheit(self._environment.inlet_temperature)

        # Q(t) is nonzero if heating element in on, else zero
        q = self.configuration.power_input if self.heater_is_on() else 0.0

        inside = g * ambient + b * inlet + q
        inside *= r_prime

        result = to_fahrenheit(last_temperature) * scalar + inside * (1 - scalar)
        return to_celsius(result)

    def update(self):
        last_temperature = self._temperature
        self._current_demand = randomize_demand(self._environment.demand/self._environment.time_scaling_factor)
        self._temperature = self.new_temperature(last_temperature)

        # turn on/off heater if temperature out of desired range
        if self.heater_needs_to_turn_off():
            self._on_state = OnState.OFF
        elif self.heater_needs_to_turn_on():
            self._on_state = OnState.ON

    def info(self, include_config=False):
        d = {
            'current_temperature': self._temperature,
            'current_lower_limit': self._lower_limit,
            'current_demand': self._current_demand,
            'current_state': str(self._on_state),
            'id': self._hid,
        }

        if include_config:
            d['configuration'] = self.configuration.info()

        return d

    def data_output(self):
        return {
            'temperature': float(self._temperature),
            'on_state': 1 if self.heater_is_on() else 0,
            'demand': float(self._current_demand),
            'inlet': float(self._environment.inlet_temperature),
            'ambient': float(self._environment.ambient_temperature),
        }

def randomize_demand(demand):
    """Return a randomized demand when given a static demand"""
    return random.uniform(0, 2) * demand

def make_heater(size, env=None, hid=None, randomize=False):
    c = config.HeaterConfiguration(tank_size=size)
    return ElectricWaterHeater(configuration=c, env=env, hid=hid, randomize=randomize)

def to_celsius(fahrenheit):
    """Convert degrees Fahrenheit to degrees Celsius"""
    return (fahrenheit - 32)/1.8

def to_fahrenheit(celsius):
    """Convert degrees Celsius to degrees Fahrenheit"""
    return (celsius * 1.8) + 32

def to_gallons(litres):
    """Convert metric litres to US gallons"""
    return 0.264172052 * litres

def to_litres(gallons):
    """Convert US gallons to metric litres"""
    return 3.78541 * gallons
