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

    def run(self, subset_divider=None, subset_size=None, output_csv=True):
        if subset_divider is None:
            subset_divider = lambda population: (population, [])  # use identity function

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
        logging.info('Time Step {0} (total hour {1}) (day {2} hour {3})'.format(time_step_index, self._environment.current_hour, *self._environment.time_tuple))

        if (time_step_index % self._hub_interval) == 0:
            # calc and send some messages
            peak_message = ' - PEAK PERIOD' if self._environment.is_in_peak_period() else None
            off_message = ' - OFF PEAK' if self._environment.is_in_immediate_non_peak_period else None
            logging.info('Hub{0}'.format(peak_message or off_message or ''))

            # TODO: clean this up
            if self._environment.is_in_peak_period():
                self.send_and_poll(self._population, [], [])
            elif self._environment.is_in_immediate_non_peak_period():
                self.send_and_poll([], self._population, [])
            else:
                self.send_and_poll([], [], self._population)
        else:
            # hub does nothing this step - just update temperatures in ewhs
            logging.info('Non-hub')
            self.send_and_poll([], [], self._population)

    def send_and_poll(self, low_power_subset, regular_power_subset, unused_subset):
        all_temps = []
        total_on = 0
        total_low = 0

        # TODO: clean this up
        for c in low_power_subset:
            c.receive_low_power_signal()  # send LOW
            data = c.data_output()
            all_temps.append(data['temperature'])
            total_on += data['on_state']
            total_low += data['usage_state']

        for c in regular_power_subset:
            c.receive_regular_power_signal()
            data = c.data_output()
            all_temps.append(data['temperature'])
            total_on += data['on_state']
            total_low += data['usage_state']

        for c in unused_subset:
            c.poll()  # don't receive anything
            data = c.data_output()
            all_temps.append(data['temperature'])
            total_on += data['on_state']
            total_low += data['usage_state']

        mean = truncate_float(statistics.mean(all_temps))

        self._population_mapping.append({
            'temperature': mean,  # mean average temperature
            'total_on': total_on,
            'total_low': total_low,
            'inlet': self._environment.inlet_temperature,
            'ambient': self._environment.ambient_temperature,
            'demand': self._environment.demand,
            'temp_pstdev': truncate_float(statistics.pstdev(all_temps, mu=mean)),
            'temp_median': truncate_float(statistics.median(all_temps)),
            #'temp_mode': truncate_float(statistics.mode(all_temps)),
            'temp_lowest': truncate_float(min(all_temps)),
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

def build_small_tank_population(population_size, env):
    return [controller.make_controller_and_heater(TankSize.SMALL, env=env, cid=i, randomize=True) for i in range(population_size)]

def build_large_tank_population(population_size, env):
    return [controller.make_controller_and_heater(TankSize.LARGE, env=env, cid=i, randomize=True) for i in range(population_size)]

def output_population_to_csv(mapping, csv_directory):
    fieldnames = ('time_step', 'temperature', 'total_on', 'total_low', 'inlet', 'ambient', 'demand', 'temp_pstdev', 'temp_median', 'temp_lowest')
    location = os.path.join(csv_directory, 'population.csv')
    with open(location, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for time_step_index, data in enumerate(mapping):
            writer.writerow(dict({'time_step': time_step_index}, **data))
