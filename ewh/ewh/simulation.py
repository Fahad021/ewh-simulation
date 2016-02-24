import itertools
import random
import logging
import pprint

import environment
import ewh
import controller
from states import TankSize

class SimulationHub(object):
    def __init__(self, **kwargs):
        self._environment = environment.setup_environment(kwargs['csv_location'])

        if kwargs['tank_size'] == TankSize.SMALL:
            builder = build_small_tank_population
        else:
            builder = build_large_tank_population
        self._population = builder(kwargs['population_size'])

        random.seed(kwargs['seed'])

        self._time_step_range = make_range(args['start_time_step'], args['end_time_step'])

    def run(self, subset_divider=None, subset_size=None):
        if subset_divider is None:
            subset_divider = lambda population, subset_size: (population, [])  # use identity function

        for time_step_index in self._time_step_range:
            self._environment.sync_timestep(time_step_index)
            info = pprint.pformat(self._environment.info())
            logging.info('Time Step {0}, Environment: {1}'.format(time_step_index, info))
            run_time_step(*subset_divider(self._population))

    def run_time_step(self, used_subset, unused_subset):
        pass

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

def build_small_tank_population(population_size):
    return [controller.Controller(ewh.make_small_ewh()) for _ in range(population_size)]

def build_large_tank_population(population_size):
    return [controller.Controller(ewh.make_large_ewh()) for _ in range(population_size)]
