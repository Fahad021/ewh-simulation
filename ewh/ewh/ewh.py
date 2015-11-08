from states import OnState
import config

import time


class ElectricWaterHeater(object):
    def __init__(self, state=State.OFF, configuration=None):
        self._on_state = state
        if configuration is None:
            self._config = config.HeaterConfiguration()  # use default
        else:
            self._config = configuration

        self._init_time = time.time()
        self._last_poll_time = self._init_time
        self._total_time_on = 0
        self._time_on_since_last_poll = 0
        self._top_temperature = self.configuration.initial_tank_temperature
        self._bottom_temperature = self.configuration.initial_tank_temperature
        self._lower_limit = self.configuration.regular_power_temp

    def update_temperatures(self):
        """
        Get the current temperature of the water in the tank.
        This is a function of the ambient temperature of the air surrounding the
        tank, the inlet water temperature, previous temperature of the water,
        time elapsed, the usage rate, the size of the tank, and the tank's
        insulation efficiency.
        """
        # right now - if on, add 5 deg per hour, if off subtract one per hour
        # TODO: this completely changed with the top/bottom configuration
        pass

    @property
    def configuration(self):
        return self._config

    @configuration.setter
    def configuration(self, c):
        self._config = c

    @property
    def total_time_on(self):
        return self._total_time_on

    def go_to_low_power_mode(self):
        self._lower_limit = self.configuration.low_power_temp

    def got_to_regular_power_mode(self):
        self._lower_limit = self.configuration.regular_power_temp

    def bottom_needs_power(self):
        return self._bottom_temperature < self._lower_limit

    def top_needs_power(self):
        return self._top_temperature < self.configuration.regular_power_temp

    def switch_power(self, state):
        self._on_state = state

    def info(self, include_config=False):
        d = {
            'current_top_temperature': self._top_temperature,
            'current_bottom_temperature': self._bottom_temperature,
            'current_bottom_tank_lower_limit': self._lower_limit,
            'total_time_on': self._total_time_on
            'state': str(self._on_state),
        }

        if include_config:
            d['configuration'] = self.configuration.info()

        return d
