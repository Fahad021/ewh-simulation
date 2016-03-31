from states import TankSize

DESIRED_TEMPERATURE = 75  # in celcius
REGULAR_POWER_LOWER_LIMIT = 70
LOW_POWER_LOWER_LIMIT = 65 # absolute lowest temp (in C) before EWH must turn itself back on
INSULATION_THERMAL_RESISTANCE = 1

SPECIFIC_HEAT_OF_WATER = 1

class HeaterConfiguration(object):
    def __init__(self,
                desired_temperature=DESIRED_TEMPERATURE,
                low_power_temperature=LOW_POWER_LOWER_LIMIT,
                regular_power_temperature=REGULAR_POWER_LOWER_LIMIT,
                tank_size=TankSize.SMALL):
        self._desired_temperature = desired_temperature
        self._low_power_temperature = low_power_temperature
        self._regular_power_temperature = regular_power_temperature

        if tank_size == TankSize.SMALL:
            # 180 liter tank
            self._tank_surface_area = 2.69172 # meters^2
            self._tank_radius = 0.28 # meters
            self._tank_height = 1.25
            self._heating_element_rating = 2.8  # kW
            self._tank_gallons = 47.551  # gallons (=180L)
        else:
            # 270 liter tank
            self._tank_surface_area = 3.43062
            self._tank_radius = 0.30
            self._tank_height = 1.52
            self._heating_element_rating = 4.2
            self._tank_gallons = 71.3265  # gallons (=270L)

    def __eq__(self, given_configuration):
        return self.info() == given_configuration.info()

    def info(self):
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temperature,
            'desired_temperature': self.desired_temperature,
            'regular_mode_temperature_lower_limit': self.regular_power_temperature,
            'tank_surface_area': self.tank_surface_area,
            'tank_radius': self.tank_radius,
            'tank_height': self.tank_height,
            'insulation_thermal_resistance': self.insulation_thermal_resistance,
            'tank_gallons': self.tank_gallons,
        }

    @property
    def desired_temperature(self):
        """Upper limit of tank temperature during REGULAR power usage mode, in degC"""
        return self._desired_temperature

    @property
    def low_power_temperature(self):
        """Lower limit of tank temperature during LOW power usage mode, in degC"""
        return self._low_power_temperature

    @property
    def regular_power_temperature(self):
        """Lower limit of tank temperature during REGULAR power usage mode, in degC"""
        return self._regular_power_temperature

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
    def initial_tank_temperature(self):
        """Tank temperature on initialization in degC"""
        return self._initial_temperature

    @property
    def insulation_thermal_resistance(self):
        """Thermal resistance of tank insulation in h ft^2 degF/Btu"""
        return INSULATION_THERMAL_RESISTANCE

    @property
    def power_input(self):
        """Power input to the tank in btu/hour"""
        return 3412.1 * self._heating_element_rating

    @property
    def tank_gallons(self):
        """Size of the tank in gallons"""
        return self._tank_gallons
