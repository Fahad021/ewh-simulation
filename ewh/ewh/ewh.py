from states import OnState, TankSize
import config
import environment

import time
import math
import logging
import pprint
import random

class ElectricWaterHeater(object):
    """Represents an EWH object in the simulation. This controls whether or not
the heating elements are on or off, and changes the temperature of the tank
according to input demand, inlet/ambient temperature, and heating element state.
    """
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
        self._lower_limit = self.configuration.regular_power_lower_limit
        self._upper_limit = self.configuration.regular_power_upper_limit

        if randomize:
            # set temperature somewhere within deadband
            self._temperature = random.uniform(self.configuration.regular_power_lower_limit, self.configuration.regular_power_upper_limit)
        else:
            # set to desired temperature
            self._temperature = self.configuration.regular_power_upper_limit

    @property
    def configuration(self):
        """Configuration for this heater"""
        return self._config

    def go_to_low_power_mode(self):
        """Change temperature deadband to (low, low_upper)"""
        self._lower_limit = self.configuration.low_power_lower_limit
        self._upper_limit = self.configuration.low_power_upper_limit

    def go_to_regular_power_mode(self):
        """Change temperature deadband to (regular, desired)"""
        self._lower_limit = self.configuration.regular_power_lower_limit
        self._upper_limit = self.configuration.regular_power_upper_limit

    def heater_needs_to_turn_off(self):
        """Return True if heater is on and is OK to turn off"""
        return (self._on_state == OnState.ON) and (self._temperature >= self._upper_limit)

    def heater_needs_to_turn_on(self):
        """Return True if heater is off and is OK to turn on"""
        return (self._on_state == OnState.OFF) and (self._temperature < self._lower_limit)

    def heater_is_on(self):
        """Return True if heating element is on"""
        return self._on_state == OnState.ON

    def new_temperature(self, last_temperature):
        """Given the temperature at the last timestep, calculate a new temperature
        according to the solution to the PDE in the Dolan/Nehrir/Gerez paper"""
        # G = surface area [ft^2] / thermal resistance of tank insulation [h ft^2 F/Btu]
        g = to_square_feet(self.configuration.tank_surface_area) / self.configuration.insulation_thermal_resistance
        # B(t) = demand [Gal] * 8.3 * (specific heat of water = 1)
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
        """Refresh temperature readings and on/off state for the current timestep"""
        last_temperature = self._temperature
        self._current_demand = randomize_demand(self._environment.demand/self._environment.time_scaling_factor)
        self._temperature = self.new_temperature(last_temperature)

        # turn on/off heater if temperature out of desired range
        if self.heater_needs_to_turn_off():
            self._on_state = OnState.OFF
        elif self.heater_needs_to_turn_on():
            self._on_state = OnState.ON

    def data_output(self):
        """CSV output for this heater at the current timestep"""
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
    """Create a heater object of a given size"""
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

def to_square_feet(square_metres):
    """Convert metres^2 to ft^2"""
    return square_metres * 10.7639
