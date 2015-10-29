from unittest import TestCase

from ewh import ElectricWaterHeater
from states import State, PowerUsage
import config

class EWHTests(TestCase):
    def assertOnRegular(self, ewh):
        self.assertEqual(ewh.states, (State.ON, PowerUsage.REGULAR))

    def assertOffRegular(self, ewh):
        self.assertEqual(ewh.states, (State.OFF, PowerUsage.REGULAR))

    def test_create_ewh_in_off_regular_state(self):
        ewh = ElectricWaterHeater()
        self.assertEqual(ewh.states, (State.OFF, PowerUsage.REGULAR))

    def test_default_configuration(self):
        self.assertEqual(ElectricWaterHeater().configuration, config.Configuration())

    def test_turn_on_and_off(self):
        ewh = ElectricWaterHeater()
        original_power = ewh.total_power_usage

        # first try turning off when already off - no change in power
        ewh.turn_off()
        self.assertOffRegular(ewh)
        self.assertEqual(original_power, ewh.total_power_usage)

        # now turn on - one state change
        ewh.turn_on()
        self.assertOnRegular(ewh)
        self.assertEqual(ewh.total_power_usage, config.ACTION_POWER_CONSUMPTION)

        # turn on again, no power usage
        ewh.turn_on()
        self.assertOnRegular(ewh)
        self.assertEqual(ewh.total_power_usage, config.ACTION_POWER_CONSUMPTION)

        # turn off - another state change
        ewh.turn_off()
        self.assertOffRegular(ewh)
        self.assertEqual(ewh.total_power_usage, 2*config.ACTION_POWER_CONSUMPTION)
