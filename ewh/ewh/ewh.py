from states import OnState
import config
import simulation

import time
import math


class ElectricWaterHeater(object):
    def __init__(self, state=OnState.OFF, configuration=None, environment=None):
        self._on_state = state
        if configuration is None:
            self._config = config.HeaterConfiguration()  # use default
        else:
            self._config = configuration

        if environment is None:
            self._environment = simulation.environment()
        else:
            self._environment = environment

        self._total_time_on = 0
        self._temperature = self.configuration.initial_tank_temperature
        self._lower_limit = self.configuration.regular_power_temp

    @property
    def configuration(self):
        return self._config

    @configuration.setter
    def configuration(self, c):
        self._config = c

    @property
    def environment(self):
        return self._environment

    @property
    def total_time_on(self):
        return self._total_time_on

    def go_to_low_power_mode(self):
        self._lower_limit = self.configuration.low_power_temp

    def got_to_regular_power_mode(self):
        self._lower_limit = self.configuration.regular_power_temp

    def heater_needs_to_turn_off(self):
        return (self._on_state == OnState.ON) and (self._temperature >= self.configuration.desired_temp)

    def heater_needs_to_turn_on(self):
        return (self._on_state == OnState.OFF) and (self._temperature < self._lower_limit)

    def needs_regular_power_mode(self):
        return self._temperature < self._lower_limit

    def switch_power(self, state):
        self._on_state = state

    def convection_losses(self, current_temperature):
        """Calculate the amount of heat lost per hour due to the temperature
        difference between the tank and the air around it.
        imperial btu/hour
        """
        sa = self.configuration.tank_surface_area
        resist = 1.0 / self.configuration.insulation_thermal_resistance
        diff = current_temperature - self.environment.ambient_temperature
        return sa * resist * diff

    def demand_losses(self, current_temperature, current_demand):
        """Calculate the amount of heat lost per hour due to the incoming cold
        water.
        imperial btu/hour
        """
        scalar = 8.3 * config.SPECIFIC_HEAT_OF_WATER
        diff = current_temperature - self.environment.inlet_temperature
        return scalar * current_demand * diff

    def new_temperature(self, last_temperature, demand):
        g = self.configuration.tank_surface_area / self.configuration.insulation_thermal_resistance
        b = demand * 8.3 * config.SPECIFIC_HEAT_OF_WATER
        r_prime = 1.0 / (g + b)
        scalar = math.exp(-config.TIME_SCALING_FACTOR/r_prime)

        inside = g * self.environment.ambient_temperature + b * self.environment.inlet_temperature + self.configuration.power_input
        inside *= r_prime

        return last_temperature * scalar + inside * (1 - scalar)

    def update(self):
        last_temperature = self._temperature
        demand = 0  # TODO: tie this in from graphs

        self._temperature = self.new_temperature(last_temperature, demand)

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

def make_small_ewh():
    pass

def make_large_ewh():
    pass
