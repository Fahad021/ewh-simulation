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
    def __init__(self,
                desired_temp=DESIRED_TEMPERATURE,
                low_power_temp=LOW_POWER_LOWER_LIMIT,
                regular_power_temp=REGULAR_POWER_LOWER_LIMIT,
                tank_size=TANK_SIZE,
                ambient_temp=AMBIENT_TEMP,
                kwh=AVERAGE_KWH,
                inlet_temp=INLET_TEMP,
                initial_tank_temperature=INITIAL_TANK_TEMPERATURE,
                action_power=ACTION_POWER_CONSUMPTION):
        self._desired_temp = desired_temp
        self._low_power_temp = low_power_temp
        self._regular_power_temp = regular_power_temp
        self._tank_size = tank_size
        self._ambient_temp = ambient_temp
        self._kwh = kwh
        self._inlet_temp = inlet_temp
        self._initial_temperature = initial_tank_temperature
        self._action_power = action_power

    def as_dict(self):
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temp,
            'desired_temperature': self.desired_temp,
            'regular_mode_temperature_lower_limit': self.regular_power_lower_limit_temp,
            'tank_size': self.tank_size,
            'ambient_temperature': self.ambient_temp,
            'inlet_temperature': self.inlet_temp,
            'power_consumption_per_time_interval': self.kwh,
            'state_change_power_consumption': self.state_change_power_usage,
            'initial_tank_temperature': self.initial_tank_temperature,
            'temperature_factor': self.temperature_factor,
        }

    def __eq__(self, given_configuration):
        return self.as_dict() == given_configuration.as_dict()

    @property
    def desired_temp(self):
        return self._desired_temp

    @desired_temp.setter
    def desired_temp(self, temp):
        self._desired_temp = temp

    @property
    def low_power_temp(self):
        return self._low_power_temp

    @low_power_temp.setter
    def low_power_temp(self, temp):
        self._low_power_temp = temp

    @property
    def regular_power_lower_limit_temp(self):
        return self._regular_power_temp

    @regular_power_lower_limit_temp.setter
    def regular_power_lower_limit_temp(self, temp):
        self._regular_power_temp = temp

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
    def kwh(self):
        return self._kwh

    @property
    def initial_tank_temperature(self):
        return self._initial_temperature

    @property
    def state_change_power_usage(self):
        return self._action_power

    @property
    def temperature_factor(self):
        return None
