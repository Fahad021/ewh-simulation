from ewh import ElectricWaterHeater
from states import OnState, PowerUsage

class Controller(object):
    def __init__(self, ewh):
        self._usage_state = PowerUsage.REGULAR
        self._usage_state_changes = 0
        self._commands_received = 0

    def change_usage_state(self, new_state):
        if self._usage_state != new_state:
            self._usage_state = new_state
            self._usage_state_changes += 1

    def poll(self):
        """Update the EWH and state machine as if no message had been sent."""
        self._ewh.update()  # update temperature and independent heater on/off
        if self._ewh.needs_regular_power_mode():
            self.change_usage_state(PowerUsage.REGULAR)
            self._ewh.got_to_regular_power_mode()

    def receive_low_power_signal(self):
        """Simulate a command from the hub to go into low-power mode."""
        self._ewh.update()
        self.change_usage_state(PowerUsage.LOW)
        self._ewh.go_to_low_power_mode()
        self._commands_received += 1

    def receive_regular_power_signal(self):
        """Simulate a command from the hub to go into regular-power mode."""
        self._ewh.update()
        self.change_usage_state(PowerUsage.REGULAR)
        self._ewh.go_to_regular_power_mode()
        self._commands_received += 1

    def total_power_consumption(self):
        return self._usage_state_changes + self._commands_received + self._ewh.total_time_on

    def info(self, include_ewh=False):
        d = {
            'power_usage_state': str(self._usage_state),
        }

        if include_ewh:
            d['heater'] = self._ewh.info(include_config=include_config)

        return d
