from states import State, PowerUsage
import config

import time


class ElectricWaterHeater(object):
    def __init__(self, state=State.OFF, usage=PowerUsage.REGULAR, configuration=None):
        self._on_state = state
        self._usage_state = usage
        if configuration is None:
            self._configuration = config.Configuration()  # use default
        else:
            self._configuration = configuration

        self._init_time = time.time()
        self._last_tank_temperature = self.configuration.initial_tank_temperature
        self._last_poll_time = self._init_time
        self._last_power_usage = 0
        self._total_power_usage = 0

    def temperature(self):
        """
        Get the current temperature of the water in the tank.
        This is a function of the ambient temperature of the air surrounding the
        tank, the inlet water temperature, previous temperature of the water,
        time elapsed, the usage rate, the size of the tank, and the tank's
        insulation efficiency.
        """
        # right now - if on, add 5 deg per hour, if off subtract one per hour
        hours_since_last_poll = (time.time() - self._last_poll_time) / 3600
        if self._on_state == State.ON:
            delta = 5 * hours_since_last_poll
        else:
            delta = hours_since_last_poll * (-1)

        result = self._last_tank_temperature + (delta * config.TIME_SCALING_FACTOR)
        self._last_tank_temperature = result
        return result

    def power_usage_since_last_poll(self):
        return None

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, config):
        self._configuration = config

    @property
    def total_power_usage(self):
        return self._total_power_usage

    @property
    def states(self):
        return (self._on_state, self._usage_state)

    def info(self, include_config=False):
        d = {
            'total_power_usage': self.total_power_usage,
            'current_temperature': self.temperature(),
            'state': str(self._on_state),
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

    def turn_on(self):
        if self._on_state != State.ON:
            self._on_state = State.ON
            self._total_power_usage += self.configuration.state_change_power_usage

    def turn_off(self):
        if self._on_state != State.OFF:
            self._on_state = State.OFF
            self._total_power_usage += self.configuration.state_change_power_usage

    def poll(self):
        current_temp = self.temperature()
        self._last_tank_temperature = current_temp

        is_in_low_power_mode = self._usage_state == PowerUsage.LOW
        is_below_regular_threshold = current_temp < self.configuration.regular_power_lower_limit_temp
        is_below_lower_limit_threshold = current_temp < self.configuration.low_power_temp
        is_at_desired_temperature = current_temp >= self.configuration.desired_temp

        if is_in_low_power_mode and is_below_lower_limit_threshold:
            self.turn_on()
            self._usage_state = PowerUsage.REGULAR
        elif not is_in_low_power_mode and is_below_regular_threshold:
            self.turn_on()
        elif is_at_desired_temperature:
            self.turn_off()

    def receive_command(self, force=False):
        is_in_low_power_mode = self._usage_state == PowerUsage.LOW
        is_on = self._on_state == State.ON
        is_below_regular_threshold = self.temperature() < self.configuration.regular_power_lower_limit_temp

        if is_in_low_power_mode:
            pass
        else:
            self._usage_state = PowerUsage.LOW
