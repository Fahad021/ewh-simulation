from unittest import TestCase

import ewh
import config
import states
import environment

class EWHTests(TestCase):
    """This test class tests the behaviour of a single EWH unit with
    default configuration."""

    def setUp(self):
        self.heater = ewh.ElectricWaterHeater()

    def assertOn(self):
        self.assertEqual(self.heater._on_state, states.OnState.ON)

    def assertOff(self):
        self.assertEqual(self.heater._on_state, states.OnState.OFF)

    def test_given_configuration(self):
        """Check if user gives a configuration, the default one is not used."""
        given = config.HeaterConfiguration(desired_temp=1000)
        heater = ewh.ElectricWaterHeater(configuration=given)
        self.assertEqual(heater.configuration, given)
        self.assertNotEqual(heater.configuration, config.HeaterConfiguration())
        # TODO: below may not be relevant if __eq__ is not redefined
        self.assertNotEqual(heater, ewh.ElectricWaterHeater())

    def test_default_configuration(self):
        """Check if the user does not give a configuration, use the default one."""
        self.assertEqual(self.heater.configuration, config.HeaterConfiguration())

    def test_given_environment(self):
        """Check if the user gives a separate environment that we don't use the simulation-wide one."""
        enviro = environment.Environment(initial_ambient_temperature=10000, initial_inlet_temperature=10000)
        self.assertNotEqual(enviro, environment.environment())
        heater = ewh.ElectricWaterHeater(environment=enviro)
        self.assertEqual(heater.environment, enviro)
        self.assertNotEqual(heater.environment, environment.environment())

    def test_default_environment(self):
        """Check if the user does not give an environment, we use the simulation-wide one."""
        self.assertEqual(self.heater.environment, environment.environment())

    def test_default_values(self):
        """Make sure the default values are as expected."""
        self.assertOff(self.ewh)
        self.assertEqual(self.ewh.total_time_on, 0)

    def test_temperature_deadband(self):
        self.fail("write this test")

    def test_update_updates_time_steps_on(self):
        """Check that if the heater is on and an update() is called, the total time on is updated.
        Likewise, check that if it is not on that the value is the same."""
        self.fail("write this test")

    def test_update_changes_power_state_when_necessary(self):
        """Check that if the OnState of the heater needs to be changed (i.e. it is
        outside of the acceptable temperature deadband), running an update() will
        change the state accordingly. Try this with low power and regular power modes."""
        self.fail("write this test")

    def test_update_does_not_change_power_state_in_deadband(self):
        """Check that if the OnState of the heater is within the acceptable temperature
        deadband, then the heating element is not toggled. Try this with the low power
        and regular power modes."""
        self.fail("write this test")


class EnvironmentTests(TestCase):
    def test_update_inlet(self):
        env = environment.Environment()
        old_ambient = env.ambient_temperature
        new_inlet = env.inlet_temperature + 1
        env.update_environment(new_inlet=new_inlet)
        self.assertEqual(env.inlet_temperature, new_inlet)
        self.assertEqual(env.ambient_temperature, old_ambient)

    def test_update_ambient(self):
        env = environment.Environment()
        old_inlet = env.inlet_temperature
        new_ambient = env.ambient_temperature + 1
        env.update_environment(new_ambient=new_ambient)
        self.assertEqual(env.inlet_temperature, old_inlet)
        self.assertEqual(env.ambient_temperature, new_ambient)

    def test_update_both(self):
        env = environment.Environment()
        new_ambient = env.ambient_temperature - 1
        new_inlet = env.inlet_temperature + 1
        env.update_environment(new_inlet=new_inlet, new_ambient=new_ambient)
        self.assertEqual(env.inlet_temperature, new_inlet)
        self.assertEqual(env.ambient_temperature, new_ambient)

    def test_update_none(self):
        env = environment.Environment()
        old_ambient = env.ambient_temperature
        old_inlet = env.inlet_temperature
        env.update_environment()  # do nothing
        self.assertEqual(env.inlet_temperature, old_inlet)
        self.assertEqual(env.ambient_temperature, old_ambient)

    def test_environment_singleton(self):
        default_env = environment.Environment()
        singleton = environment.environment()
        self.assertEqual(singleton, default_env)
        singleton.update_environment(new_inlet=1)
        self.assertNotEqual(singleton, default_env)
        again = environment.environment()
        self.assertEqual(singleton, again)
        again.update_environment(new_inlet=2)
        self.assertEqual(singleton, again)
        self.assertNotEqual(singleton, default_env)

class ControllerTests(TestCase):
    pass
