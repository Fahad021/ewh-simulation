from ewh import ElectricWaterHeater
from states import OnState, PowerUsage
from config import ControllerConfiguration

import time

class Controller(object):
    def __init__(self, ewh=None, config=None):
        if ewh is None:
            self._ewh = ElectricWaterHeater()
        else:
            self._ewh = ewh

        if config is None:
            self._config = ControllerConfiguration()
        else:
            self._config = config

        self._on_state = OnState.OFF
        self._usage_state = PowerUsage.REGULAR
        self._on_state_changes = 0
        self._usage_state_changes = 0
        self._commands_received = 0

    def change_on_state(self, new_state):
        if self._on_state != new_state:
            self._on_state = new_state
            self._on_state_changes += 1
            self._ewh.switch_power(new_state)

    def change_usage_state(self, new_state):
        if self._usage_state != new_state:
            self._usage_state = new_state
            self._usage_state_changes += 1

    def poll(self):
        self._ewh.update_temperatures()

        # first check power usage mode
        if self._usage_state == PowerUsage.LOW and self._ewh.top_needs_power():
            self._usage_state = PowerUsage.REGULAR
            self._usage_state_changes += 1
            self._ewh.got_to_regular_power_mode()

        # now check which heater needs to turn on/off
        # looks really ugly, but check state diagram
        if self._on_state == OnState.OFF and self._ewh.bottom_needs_power():
            self.change_on_state(OnState.BOTTOM)
        elif self._on_state == OnState.BOTTOM:
            if self._ewh.top_needs_power():
                self.change_on_state(OnState.TOP)
            elif not self._ewh.bottom_needs_power():
                self.change_on_state(OnState.OFF)
        elif self._on_state == OnState.TOP and not self._ewh.top_needs_power():
            if self._ewh.bottom_needs_power():
                self.change_on_state(OnState.BOTTOM)
            else:
                self.change_on_state(OnState.OFF)

    def receive_command(self):
        if self._usage_state == PowerUsage.REGULAR:
            self._usage_state = PowerUsage.LOW
            self._usage_state_changes += 1
            self._ewh.go_to_low_power_mode()
        self._commands_received += 1

    def total_power_consumption(self):
        return (self._on_state_changes +
            self._usage_state_changes +
            self._commands_received +
            self._ewh.total_time_on) * self.configuration.power_consumption

    def power_consumption_since_last_poll(self):
        pass

    def info(self, include_config=False, include_ewh=False):
        d = {
            'on_state': str(self._on_state),
            'power_usage_state': str(self._usage_state),
        }

        if include_config:
            d['configuration'] = self._config.info()

        if include_ewh:
            d['heater'] = self._ewh.info()

        return d
