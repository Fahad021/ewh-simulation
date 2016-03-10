from states import OnState, TankSize
import config
import environment

import time
import math
import logging
import pprint
import random

class ElectricWaterHeater(object):
    def __init__(self, randomize=False, state=OnState.OFF, configuration=None, env=None):
        self._on_state = state

        if configuration is None:
            configuration = config.HeaterConfiguration()  # use default
        if env is None:
            env = environment.environment()

        self._config = configuration
        self._environment = env

        self._total_time_on = 0
        self._lower_limit = self.configuration.regular_power_temperature

        if randomize:
            # set temperature somewhere within deadband
            self._temperature = random.uniform(self.configuration.low_power_temperature, self.configuration.desired_temperature)
        else:
            # set to outside temperature
            self._temperature = self._environment.ambient_temperature

        logging.debug("Initial {0}".format(pprint.pformat(self.info(include_config=True))))

    @property
    def configuration(self):
        return self._config

    @property
    def total_time_on(self):
        """Number of time steps the heater has been on since initialization"""
        return self._total_time_on

    def go_to_low_power_mode(self):
        self._lower_limit = self.configuration.low_power_temperature

    def got_to_regular_power_mode(self):
        self._lower_limit = self.configuration.regular_power_temperature

    def heater_needs_to_turn_off(self):
        return (self._on_state == OnState.ON) and (self._temperature >= self.configuration.desired_temperature)

    def heater_needs_to_turn_on(self):
        return (self._on_state == OnState.OFF) and (self._temperature < self._lower_limit)

    def heater_is_on(self):
        return self._on_state == OnState.ON

    def switch_power(self, new_state):
        logging.debug("EWH turning {0}".format(str(new_state)))
        self._on_state = new_state

    def new_temperature(self, last_temperature):
        g = self.configuration.tank_surface_area / self.configuration.insulation_thermal_resistance
        b = randomize_demand(self.environment.demand) * 8.3 * config.SPECIFIC_HEAT_OF_WATER
        r_prime = 1.0 / (g + b)
        scalar = math.exp(-self.environment.time_scaling_factor/r_prime)

        ambient = to_fahrenheit(self.environment.ambient_temperature)
        inlet = to_fahrenheit(self.environment.inlet_temperature)

        inside = g * ambient + b * self.environment.inlet_temperature + self.configuration.power_input
        inside *= r_prime

        result = to_fahrenheit(last_temperature) * scalar + inside * (1 - scalar)
        return to_celsius(result)

    def update(self):
        last_temperature = self._temperature
        self._temperature = self.new_temperature(last_temperature)

        logging.debug('EWH temperature {0} to {1}'.format(last_temperature, self._temperature))

        if self.heater_is_on():
            self._total_time_on += 1

        # turn on/off heater if temperature out of desired range
        if self.heater_needs_to_turn_off():
            self.switch_power(OnState.OFF)
        elif self.heater_needs_to_turn_on():
            self.switch_power(OnState.ON)

    def info(self, include_config=False):
        d = {
            'current_temperature': self._temperature,
            'current_lower_limit': self._lower_limit,
            'total_time_on': self._total_time_on,
            'current_state': str(self._on_state),
        }

        if include_config:
            d['configuration'] = self.configuration.info()

        return d

def randomize_demand(demand_in_litres):
    """Return a randomized demand (in gallons per hour) when given a static
    demand (in L/h)"""
    return random.uniform(0, 2) * to_gallons(demand_in_litres)

def make_small_ewh(env=None):
    c = config.HeaterConfiguration(tank_size=TankSize.SMALL)
    return ElectricWaterHeater(configuration=c, env=env)

def make_large_ewh(env=None):
    c = config.HeaterConfiguration(tank_size=TankSize.LARGE)
    return ElectricWaterHeater(configuration=c, env=env)

def to_celsius(fahrenheit):
    """Convert degrees Fahrenheit to degrees Celsius"""
    return (fahrenheit - 32)/1.8

def to_fahrenheit(celsius):
    """Convert degrees celsius to degrees Fahrenheit"""
    return (celsius * 1.8) + 32

def to_gallons(litres):
    """Convert metric litres to US gallons"""
    return 0.264172052 * litres
