from ewh import ElectricWaterHeater
from states import OnState, PowerUsage
from config import ControllerConfiguration

class Controller(object):
    def __init__(self, ewh, config=None):
        if config is None:
            self._config = ControllerConfiguration()
        else:
            self._config = config

        self._usage_state = PowerUsage.REGULAR
        self._usage_state_changes = 0
        self._commands_received = 0

    def change_usage_state(self, new_state):
        if self._usage_state != new_state:
            self._usage_state = new_state
            self._usage_state_changes += 1

    def poll(self):
        self._ewh.update()  # update temperature and independent heater on/off
        if self._ewh.needs_regular_power_mode():
            self.change_usage_state(PowerUsage.REGULAR)
            self._ewh.got_to_regular_power_mode()

    def receive_command(self):
        self._ewh.update()

        if self._usage_state == PowerUsage.REGULAR:
            self._usage_state = PowerUsage.LOW
            self._usage_state_changes += 1
            self._ewh.go_to_low_power_mode()
        self._commands_received += 1

    def total_power_consumption(self):
        return (self._usage_state_changes +
            self._commands_received +
            self._ewh.total_time_on) * self.configuration.power_consumption

    def info(self, include_config=False, include_ewh=False):
        d = {
            'power_usage_state': str(self._usage_state),
        }

        if include_config:
            d['configuration'] = self._config.info()

        if include_ewh:
            d['heater'] = self._ewh.info(include_config=include_config)

        return d
