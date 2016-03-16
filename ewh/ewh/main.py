import argparse
import os.path
import sys
import logging
import pprint
import time

from states import TankSize

import simulation
import environment

def main():
    sim = simulation.SimulationHub(**vars(parse_args()))
    sim.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="rng seed", type=int)
    parser.add_argument("--csv",
        dest="csv_directory",
        help="directory containing input csv data files",
        metavar="DIRECTORY",
        default="../Data/")
    parser.add_argument("--tank-size",
        help="heater tank size in liters",
        type=int,
        dest="tank_size")
    parser.add_argument("--population-size",
        help="number of heaters in population",
        dest="population_size",
        default=1000,
        type=int)
    parser.add_argument("--start-time-step",
        dest="start_time_step",
        default=0,
        type=int)
    parser.add_argument('--end-time-step',
        dest="end_time_step",
        type=int)
    parser.add_argument('--log-file',
        dest="log_file",
        default='simulation_log.log',
        type=str)
    parser.add_argument('--log-level',
        dest="log_level",
        choices=['INFO', 'DEBUG'],
        default="DEBUG")
    parser.add_argument('--reset-log',
        dest="reset_log",
        action="store_true")
    parser.add_argument('--hub-interval',
        help="time steps per hub recalculate/message delivery",
        dest="hub_interval",
        default=5,
        type=int)
    parser.add_argument('--scaling-factor',
        help="time steps per hour",
        default=60,  # once per minute,
        dest="time_scaling_factor",
        type=int)

    args = parser.parse_args()

    if not os.path.isdir(args.csv_directory):
        parser.error("Directory '{0}' does not exist.".format(args.csv_directory))
        sys.exit(1)

    if args.tank_size == 180:
        args.tank_size = TankSize.SMALL
    else:
        args.tank_size = TankSize.LARGE

    if args.reset_log:
        # clear the log file
        with open(args.log_file, 'w'):
            pass

    log_level = getattr(logging, args.log_level, None)
    logging.basicConfig(filename=args.log_file, level=log_level)
    logging.info("----Starting simulation at {0}----".format(time.strftime('%X %x %Z')))

    logging.info("Simulation Arguments: {0}".format(pprint.pformat(args)))
    return args

if __name__ == '__main__':
    main()
