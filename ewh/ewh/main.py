import argparse
import os
import sys
import logging
import pprint

from states import TankSize

import simulation
import environment

def main():
    environment.setup()
    sim = SimulationHub(parse_args())
    sim.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="rng seed", type=int)
    parser.add_argument("--csv",
        dest="csv_directory",
        help="directory containing input csv data files",
        metavar="DIRECTORY")
    parser.add_argument("--tank-size",
        help="heater tank size in liters",
        type=int,
        dest="tank_size")
    parser.add_argument("--population-size",
        help="number of heaters in population",
        dest="population_size",
        type=int)
    parser.add_argument("--start-time-step",
        dest="start_time_step",
        type=int)
    parser.add_argument('--end-time-step',
        dest="end_time_step",
        type=int)
    parser.add_argument('--log-file',
        dest="log_file",
        type=str)
    parser.add_argument('--log-level',
        dest="log_level",
        choices=['INFO', 'DEBUG'],
        default="DEBUG")

    args = parser.parse_args()

    if args['csv_directory'] is None:
        args['csv_directory'] = '../Data/'

    if not os.path.isdir(csv_directory):
        parser.error("Directory '{0}' does not exist.".format(csv_directory))
        sys.exit(1)

    if args['tank_size'] == 180:
        args['tank_size'] = TankSize.SMALL
    else:
        args['tank_size'] = TankSize.LARGE

    if args['population_size'] is None:
        args['population_size'] = 10000

    if args['start_time_step'] is None:
        args['start_time_step'] = 0

    # set up logging
    if args['log_file'] is None:
        args['log_file'] = 'simulation_log.log'

    log_level = getattr(logging, args['log_level'], None)
    logging.basicConfig(filename=args['log_file'], log_level)

    logging.info("Simulation Arguments: {0}".format(pprint.pformat(args)))
    return args

if __name__ == '__main__':
    main()
