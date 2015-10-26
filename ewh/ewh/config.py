ON_DEADBAND = (18, 20)  # low/high temps in celcius, obviously changing
REGULAR_POWER_LOWER_LIMIT = 12
LOW_POWER_LOWER_LIMIT = 10 # absolute lowest temp (in C) before EWH must turn itself back on
TANK_SIZE = 90  # in litres
INLET_TEMP = 10  # temperature of water (in C) at inlet
AVERAGE_KWH = 1  # average power usage (in kilowatt hours)
AMBIENT_TEMP = 20  # temperature (in C) of air outside of water heater
INITIAL_TANK_TEMPERATURE = 20
ACTION_POWER_CONSUMPTION = 1  # power usage when switching state

class Configuration(object):
    def __init__(self,
                deadband=ON_DEADBAND,
                low_power_temp=LOW_POWER_LOWER_LIMIT,
                regular_power_temp=REGULAR_POWER_LOWER_LIMIT,
                tank_size=TANK_SIZE,
                ambient_temp=AMBIENT_TEMP,
                kwh=AVERAGE_KWH,
                inlet_temp=INLET_TEMP
                initial_tank_temperature=INITIAL_TANK_TEMPERATURE,
                action_power=ACTION_POWER_CONSUMPTION):
        self.deadband = deadband
        self.low_power_temp = low_power_temp
        self._regular_power_temp = regular_power_temp,
        self.tank_size = tank_size
        self.ambient_temp = ambient_temp
        self.kwh = kwh
        self.inlet_temp = inlet_temp
        self._initial_temperature = initial_tank_temperature
        self._action_power = action_power

    def as_dict():
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temp,
            'deadband_temperature_range': "({0}->{1})".format(*self.deadband),
            'regular_mode_temperature_lower_limit': self.regular_power_temperature_lower_limit,
            'tank_size': self.tank_size,
            'ambient_temperature': self.ambient_temp,
            'inlet_temperature': self.inlet_temperature,
            'power_consumption_per_time_interval': self.kwh,
            'state_change_power_consumption': self.state_change_power_usage,
            'initial_tank_temperature': self.initial_tank_temperature,
        }

    @property
    def deadband(self):
        return self.deadband

    @deadband.setter
    def deadband(self, deadband):
        self.deadband = deadband

    @property
    def low_power_temp(self):
        return low_power_temp

    @low_power_temp.setter
    def low_power_temp(self, temp):
        self.low_power_temp = temp

    @property
    def regular_power_lower_limit_temp(self):
        return self._regular_power_temp

    @regular_power_lower_limit_temp.setter
    def regular_power_lower_limit_temp(self, temp):
        self._regular_power_temp = temp

    @property
    def tank_size(self):
        return self.tank_size

    @property
    def ambient_temp(self):
        return ambient_temp

    @ambient_temp.setter
    def ambient_temp(self, temp):
        self.ambient_temp = temp

    @property
    def inlet_temp(self):
        return self.inlet_temp

    @inlet_temp.setter
    def inlet_temp(self, temp):
        self.inlet_temp = temp

    @property
    def kwh(self):
        return self.kwh

    @property
    def initial_tank_temperature(self):
        return self._initial_temperature

    @property
    def state_change_power_usage(self):
        return self._action_power
