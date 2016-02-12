import itertools
import random

class Simulation(object):
    def __init__(self):
        self._environment = environment()
        self._hub = None
        self._population = []

    def add_controllers_to_population(self, population):
        self._population.extend(population)

    def run(self, start_time_step=0, time_steps=None, subset_divider=None, subset_size=None):
        if subset_divider is None:
            subset_divider = lambda population, subset_size: (population, [])  # use identity function

        for time_step in make_range(start_time_step, time_steps):
            run_time_step(*subset_divider(self._population))

    def run_time_step(self, used_subset, unused_subset):
        pass

    def poll_controller_bidirectional(self, controller):
        controller.poll()

        message = controller.info(include_ewh=True)

        # TODO: ... coming soon to a theatre near you

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
