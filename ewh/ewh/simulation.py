import itertools
import random
import logging
import pprint
import csv
import os.path
import statistics

import environment
import ewh
import controller
from states import TankSize

class SimulationHub(object):
    def __init__(self, **kwargs):
        self._environment = environment.setup_environment(kwargs['csv_directory'], kwargs['time_scaling_factor'])

        if kwargs['tank_size'] == TankSize.SMALL:
            builder = build_small_tank_population
        else:
            builder = build_large_tank_population
        self._population = builder(kwargs['population_size'], self._environment)

        random.seed(kwargs['seed'])

        self._time_step_range = make_range(kwargs['start_time_step'], kwargs['end_time_step'])
        self._hub_interval = kwargs['hub_interval']

        self._output_dir = None if kwargs['suppress_output'] else kwargs['output_directory']
        self._population_mapping = []

        self._divider = kwargs['subset_divider']
        self._divider_size = kwargs['subset_size']
        self._comms_population = []
        self._non_comms_population = self._population

        self._reactivation_low_population = []
        self._reactivation_low_mean = 0
        self._reactivation_high_population = []
        self._reactivation_high_mean = 0

    def run(self):
        try:
            for time_step_index in self._time_step_range:
                self.do_timestep(time_step_index)
        except KeyboardInterrupt:
            logging.info('Simulation Interrupted')
            pass  # don't throw stack trace, just write to csv and finish up
        finally:
            if self._output_dir is not None:
                logging.info('Writing to CSV at {0}'.format(self._output_dir))
                output_population_to_csv(self._population_mapping, self._output_dir)

    def do_timestep(self, time_step_index):
        self._environment.sync_timestep(time_step_index)
        logging.info('Time Step {0} (total hour {1}) (day {2} time {3}:{4})'.format(time_step_index, self._environment.current_hour, *self._environment.time_tuple))

        if (time_step_index % self._hub_interval) == 0:
            # calc and send some messages
            # TODO: clean this up
            if self._environment.is_at_peak_boundary():
                # save comms/non-comms subsets according to divider algorithm
                self._comms_population, self._non_comms_population = self._divider(self._population, self._divider_size)
                # send a LOW power signal to comms population
                self.send_and_poll(self._comms_population, [], self._non_comms_population)
            elif self._environment.is_in_reactivation_period() and self._environment.is_at_quarter_hour_boundary():
                # send a REGULAR power signal to comms population a bit at a time
                zone = self._environment.reactivation_zone()
                if zone == 0:
                    self.reactivation_zone_setters()
                self.reactivation_zone_boundary_step(zone)
            else:
                # update temps in ewh as normal
                self.send_and_poll([], [], self._population)
        else:
            # hub does nothing this step - just update temperatures in ewhs
            self.send_and_poll([], [], self._population)

    def reactivation_zone_setters(self):
        comms_mean = mean([c.temperature for c in self._comms_population])
        self._reactivation_low_population = [c for c in self._comms_population if c.temperature <= comms_mean]
        self._reactivation_high_population = [c for c in self._comms_population if c.temperature > comms_mean]
        self._reactivation_low_mean = mean([c.temperature for c in self._reactivation_low_population])
        self._reactivation_high_mean = mean([c.temperature for c in self._reactivation_high_population])

    def reactivation_zone_boundary_step(self, zone):
        if zone == 0:
            [c.receive_regular_power_signal() for c in self._reactivation_low_population if c.temperature <= self._reactivation_low_mean]
        elif zone == 1:
            [c.receive_regular_power_signal() for c in self._reactivation_low_population if c.temperature > self._reactivation_low_mean]
        elif zone == 2:
            [c.receive_regular_power_signal() for c in self._reactivation_high_population if c.temperature <= self._reactivation_high_mean]
        elif zone == 3:
            [c.receive_regular_power_signal() for c in self._reactivation_high_population if c.temperature <= self._reactivation_high_mean]

    def send_and_poll(self, low_power_subset, regular_power_subset, unused_subset):
        all_temps = []
        all_demands = []
        comms_temps = []
        non_comms_temps = []
        comms_on = 0
        non_comms_on = 0
        total_low = 0

        # TODO: clean this up
        for c in low_power_subset:
            c.receive_low_power_signal()  # send LOW
            data = c.data_output()
            all_temps.append(data['temperature'])
            all_demands.append(data['demand'])
            comms_temps.append(data['temperature'])
            comms_on += data['on_state']
            total_low += data['usage_state']

        for c in regular_power_subset:
            c.receive_regular_power_signal()  # send REGULAR
            data = c.data_output()
            all_temps.append(data['temperature'])
            all_demands.append(data['demand'])
            comms_temps.append(data['temperature'])
            comms_on += data['on_state']
            total_low += data['usage_state']

        total_comms = len(low_power_subset) + len(regular_power_subset)
        total_non_comms = len(unused_subset)

        for c in unused_subset:
            c.poll()  # don't receive anything
            data = c.data_output()
            all_temps.append(data['temperature'])
            all_demands.append(data['demand'])
            non_comms_temps.append(data['temperature'])
            non_comms_on += data['on_state']
            total_low += data['usage_state']

        total_on = non_comms_on + comms_on
        all_mean = statistics.mean(all_temps)
        try:
            comms_mean = statistics.mean(comms_temps)
        except statistics.StatisticsError:
            comms_mean = 0
            comms_pstdev = 0
        else:
            comms_pstdev = statistics.pstdev(comms_temps, mu=comms_mean)

        try:
            non_comms_mean = statistics.mean(non_comms_temps)
        except statistics.StatisticsError:
            non_comms_mean = 0
            non_comms_pstdev = 0
        else:
            non_comms_pstdev = statistics.pstdev(non_comms_temps, mu=non_comms_mean)

        self._population_mapping.append({
            'temperature': all_mean,  # mean average temperature
            'total_on': total_on,  # total number of heaters in ON state
            'total_low': total_low,  # total number of controllers in LOW state
            'inlet': self._environment.inlet_temperature,
            'ambient': self._environment.ambient_temperature,
            'demand': statistics.mean(all_demands),
            'temp_pstdev': statistics.pstdev(all_temps, mu=all_mean), # population standard deviation of all temperatures
            'temp_median': statistics.median(all_temps),
            'temp_lowest': min(all_temps),
            'temp_highest': max(all_temps),
            'comms_on': comms_on,  # number of controllers with communications in ON state
            'non_comms_on': non_comms_on,  # number of controllers without communcations in ON state
            'total_population_size': total_comms + total_non_comms,
            'total_comms_population_size': total_comms,  # number of controllers with communication capabilities
            'comms_temps_mean': comms_mean,
            'comms_temps_pstdev': comms_pstdev,
            'comms_temps_lowest': min(comms_temps, default=0),
            'comms_temps_highest': max(comms_temps, default=0),
            'non_comms_mean': non_comms_mean,
            'non_comms_temps_pstdev': non_comms_pstdev,
            'non_comms_temps_lowest': min(non_comms_temps, default=0),
            'non_comms_temps_highest': max(non_comms_temps, default=0),
        })

def truncate_float(f, places=2):
    return float("{0:.{1}f}".format(f, places))

def make_range(start, end):
    """Return a generator of the time steps to iterate over"""
    if end is None:
        return itertools.count(start=start, step=1)
    else:
        return range(start, end)

def randomize_subset_constant_size(population, constant_subset_size):
    """Return a tuple containing a random subset of an iterable of given size
    and its set complement."""
    subset = random.sample(population, constant_subset_size)
    return (subset, set(population) - set(subset))

def randomize_subset_variable_limited_size(population, max_subset_size):
    """Return a tuple containing a random subset of an iterable of a random size
    and its set complement."""
    if max_subset_size > len(population):
        max_subset_size = len(population)
    return randomize_subset_constant_size(population, random.randint(0, max_subset_size))

def entire_population(population, size):
    return (population, [])

def mean(population):
    try:
        return statistics.mean(population)
    except statistics.StatisticsError:
        return 0

def build_small_tank_population(population_size, env):
    return [controller.make_controller_and_heater(TankSize.SMALL, env=env, cid=i, randomize=True) for i in range(population_size)]

def build_large_tank_population(population_size, env):
    return [controller.make_controller_and_heater(TankSize.LARGE, env=env, cid=i, randomize=True) for i in range(population_size)]

def output_population_to_csv(mapping, csv_directory):
    fieldnames = ('time_step',
        'temperature',
        'total_on',
        'total_low',
        'inlet',
        'ambient',
        'demand',
        'temp_pstdev',
        'temp_median',
        'temp_lowest',
        'temp_highest',
        'comms_on',
        'non_comms_on',
        'total_population_size',
        'total_comms_population_size',
        'comms_temps_mean',
        'comms_temps_pstdev',
        'comms_temps_lowest',
        'comms_temps_highest',
        'non_comms_mean',
        'non_comms_temps_pstdev',
        'non_comms_temps_lowest',
        'non_comms_temps_highest')
    location = os.path.join(csv_directory, 'population.csv')
    with open(location, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for time_step_index, data in enumerate(mapping):
            writer.writerow(dict({'time_step': time_step_index}, **data))
