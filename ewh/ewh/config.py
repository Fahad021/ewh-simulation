DESIRED_TEMPERATURE = 55  # in celcius
REGULAR_POWER_LOWER_LIMIT = 50
LOW_POWER_LOWER_LIMIT = 45 # absolute lowest temp (in C) before EWH must turn itself back on
TANK_SIZE = 270  # in litres
INLET_TEMP = 10  # temperature of water (in C) at inlet
AVERAGE_KWH = 1  # average power usage (in kilowatt hours)
AMBIENT_TEMP = 20  # temperature (in C) of air outside of water heater
INITIAL_TANK_TEMPERATURE = 20
ACTION_POWER_CONSUMPTION = 1  # power usage when switching state

TIME_SCALING_FACTOR = 1


class Configuration(object):
    def __eq__(self, given_configuration):
        return self.info() == given_configuration.info()


class ControllerConfiguration(Configuration):
    def __init__(self,
                 power_usage=AVERAGE_KWH,
                 action_power=ACTION_POWER_CONSUMPTION):
        self._kwh = kwh
        self._action_power = action_power

    def info(self):
        return {
            'power_consumption': self.power_consumption,
            'state_change_power_consumption': self.state_change_power_consumption,
        }

    @property
    def power_consumption(self):
        return self._kwh

    @property
    def state_change_power_consumption(self):
        return self._action_power


class HeaterConfiguration(Configuration):
    # TODO: consistent naming (temp vs temperature)
    def __init__(self,
                desired_temp=DESIRED_TEMPERATURE,
                low_power_temp=LOW_POWER_LOWER_LIMIT,
                regular_power_temp=REGULAR_POWER_LOWER_LIMIT,
                tank_size=TANK_SIZE,
                ambient_temp=AMBIENT_TEMP,
                inlet_temp=INLET_TEMP,
                initial_tank_temperature=INITIAL_TANK_TEMPERATURE):
        self._desired_temp = desired_temp
        self._low_power_temp = low_power_temp
        self._regular_power_temp = regular_power_temp
        self._tank_size = tank_size
        self._ambient_temp = ambient_temp
        self._inlet_temp = inlet_temp
        self._initial_temperature = initial_tank_temperature

    def info(self):
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temp,
            'desired_temperature': self.desired_temp,
            'regular_mode_temperature_lower_limit': self.regular_power_temp,
            'tank_size': self.tank_size,
            'ambient_temperature': self.ambient_temp,
            'inlet_temperature': self.inlet_temp,
            'initial_tank_temperature': self.initial_tank_temperature,
        }

    @property
    def desired_temp(self):
        return self._desired_temp

    @desired_temp.setter
    def desired_temp(self, temp):
        self._desired_temp = temp

    @property
    def low_power_temp(self):
        return self._low_power_temp

    @property
    def regular_power_temp(self):
        return self._regular_power_temp

    @property
    def tank_size(self):
        return self._tank_size

    @property
    def ambient_temp(self):
        return self._ambient_temp

    @ambient_temp.setter
    def ambient_temp(self, temp):
        self._ambient_temp = temp

    @property
    def inlet_temp(self):
        return self._inlet_temp

    @inlet_temp.setter
    def inlet_temp(self, temp):
        self._inlet_temp = temp

    @property
    def initial_tank_temperature(self):
        return self._initial_temperature
