DESIRED_TEMPERATURE = 55  # in celcius
REGULAR_POWER_LOWER_LIMIT = 50
LOW_POWER_LOWER_LIMIT = 45 # absolute lowest temp (in C) before EWH must turn itself back on
TANK_SURFACE_AREA = 0  # in square meters
TANK_RADIUS = 0  # in meters
TANK_HEIGHT = 0  # in meters
INLET_TEMP = 10  # temperature of water (in C) at inlet
AVERAGE_KWH = 1  # average power usage (in kilowatt hours)
AMBIENT_TEMP = 20  # temperature (in C) of air outside of water heater
INITIAL_TANK_TEMPERATURE = 20
ACTION_POWER_CONSUMPTION = 1  # power usage when switching state
INSULATION_THERMAL_RESISTANCE = 1

TIME_SCALING_FACTOR = 1
SPECIFIC_HEAT_OF_WATER = 1
HEATING_ELEMENT_RATING_270_LITER = 4.2  # kW
HEATING_ELEMENT_RATING_180_LITER = 2.8  # kW


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
                tank_surface_area=TANK_SURFACE_AREA,
                tank_radius=TANK_RADIUS,
                tank_height=TANK_HEIGHT,
                ambient_temp=AMBIENT_TEMP,
                inlet_temp=INLET_TEMP,
                initial_tank_temperature=INITIAL_TANK_TEMPERATURE
                heating_element_rating=HEATING_ELEMENT_RATING_270_LITER):
        self._desired_temp = desired_temp
        self._low_power_temp = low_power_temp
        self._regular_power_temp = regular_power_temp
        self._tank_surface_area = tank_surface_area
        self._tank_radius = tank_radius
        self._tank_height = tank_height
        self._ambient_temp = ambient_temp
        self._inlet_temp = inlet_temp
        self._initial_temperature = initial_tank_temperature
        self._heating_element_rating = heating_element_rating

    def info(self):
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temp,
            'desired_temperature': self.desired_temp,
            'regular_mode_temperature_lower_limit': self.regular_power_temp,
            'tank_surface_area': self.tank_surface_area,
            'tank_radius': self.tank_radius,
            'tank_height': self.tank_height,
            'tank_size': self.tank_size,
            'ambient_temperature': self.ambient_temp,
            'inlet_temperature': self.inlet_temp,
            'initial_tank_temperature': self.initial_tank_temperature,
            'insulation_thermal_resistance': self.insulation_thermal_resistance,
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
    def tank_surface_area(self):
        """Surface area of the outside of the water tank, in square meters"""
        return self._tank_surface_area

    @property
    def tank_radius(self):
        """Radius of the water tank, in meters"""
        return self._tank_radius

    @property
    def tank_height(self):
        """Height of the water tank, in meters"""
        return self._tank_height

    @property
    def tank_size(self):
        """Total size of the water tank, in liters"""
        return self.tank_radius * self.tank_height

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

    @property
    def insulation_thermal_resistance(self):
        return INSULATION_THERMAL_RESISTANCE

    @property
    def power_input(self):
        """Power input to the tank in btu/hour"""
        return 3412.1 * self._heating_element_rating
