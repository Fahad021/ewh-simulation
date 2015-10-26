from .states import State, PowerUsage
from . import config

import time

class ElectricWaterHeater(object):
    def __init__(self, state=State.OFF, usage=PowerUsage.REGULAR, config=None):
        self._on_state = state
        self._usage_state = usage
        if config is None:
            self.configuration = config.Configuration()  # use default
        else:
            self.configuration = config

        self._init_time = time.time()
        self._last_tank_temperature = self.configuration.initial_tank_temperature
        self._last_power_usage = 0
        self._total_power_usage = 0

    def temperature(self):
        """
        Get the current temperature of the water in the tank.
        This is a function of the ambient temperature of the air surrounding the
        tank, the inlet water temperature, previous temperature of the water,
        the usage rate, the size of the tank, and the tank's insulation efficiency.
        """
        return config.inlet_tem

    def power_usage_since_last_poll(self):
        return None

    @property
    def total_power_usage(self):
        return self._total_power_usage

    def info(self, include_config=False):
        d = {
            'total_power_usage': self.total_power_usage,
            'current_temperature': self.temperature,
            'state': 'ON' if self._on_state == State.ON else 'OFF',
            'mode': 'LOW_POWER' if self._usage_state == PowerUsage.LOW else 'REGULAR',
        }

        if include_config:
            d['configuration'] = self.configuration.as_dict()

        return d

    def toggle_on_off(self):
        if self._on_state == State.ON:
            self._on_state = State.OFF
        else:
            self._on_state = State.ON

        self._total_power_usage += self.configuration.state_change_power_usage

    def poll(self):
        current_temp = self.temperature()
        self._last_tank_temperature = current_temp

        is_in_low_power_mode = self._usage_state == PowerUsage.LOW
        is_below_regular_threshold = current_temp < self.configuration.regular_power_lower_limit_temp
        is_below_lower_limit_threshold = current_temp < self.configuration.low_power_temp
        is_in_deadband = current_temp in range(*self.configuration.deadband)

        if is_in_low_power_mode and is_below_lower_limit_threshold:
            self._on_state = State.ON
            self._usage_state = PowerUsage.REGULAR
        elif not is_in_low_power_mode and is_below_regular_threshold:
            self._on_state = State.ON
        elif is_in_deadband:
            self._on_state = State.OFF

    def receive_command(self, force=False):
        is_in_low_power_mode = self._usage_state == PowerUsage.LOW
        is_on = self._on_state == State.ON
        is_below_regular_threshold = self.temperature() < self.configuration.regular_power_lower_limit_temp

        if is_in_low_power_mode:
            pass
        else:
            self._usage_state = PowerUsage.LOW
