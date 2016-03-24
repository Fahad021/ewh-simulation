import argparse
from os import path, mkdir
import sys
import logging
import pprint
import time
import uuid

from states import TankSize

import simulation
import environment

def main():
    sim = simulation.SimulationHub(**vars(parse_args()))
    sim.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="rng seed", type=int)
    parser.add_argument("--input-csv",
        dest="csv_directory",
        help="directory containing input csv data files",
        metavar="DIRECTORY",
        default="../Data/")
    parser.add_argument("--tank-size",
        help="heater tank size in litres",
        metavar="TANK_SIZE_IN_LITRES",
        type=int,
        dest="tank_size")
    parser.add_argument("--population-size",
        help="number of heaters in population",
        dest="population_size",
        metavar="NUM_HEATERS",
        default=3,
        type=int)
    parser.add_argument("--start-time-step",
        dest="start_time_step",
        metavar="START",
        default=0,  # start at 00:00 on January 1st
        type=int)
    parser.add_argument('--end-time-step',
        metavar="END",
        dest="end_time_step",
        default=1440,  # run for one day
        type=int)
    parser.add_argument('--log-file',
        dest="log_file",
        default='simulation_log.log',
        help="name of output log file",
        metavar="OUTPUT_LOG",
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
        metavar="HUB_INTERVAL",
        default=5,
        type=int)
    parser.add_argument('--scaling-factor',
        help="time steps per hour",
        default=60,  # once per minute,
        dest="time_scaling_factor",
        metavar="TSF",
        type=int)
    parser.add_argument('--suppress-output',
        help="don't output to csv on exit, useful when debugging",
        dest="suppress_output",
        action="store_true")
    parser.add_argument('--output-directory',
        dest="output_directory",
        help="name of csv output directory",
        type=str,
        metavar="DIR_NAME",
    )

    args = parser.parse_args()

    if not path.isdir(args.csv_directory):
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

    if not args.suppress_output:
        if args.output_directory is None:
            args.output_directory = "{0}".format(time.strftime("%Y%m%d-%H%M%S"))
        try:
            mkdir(args.output_directory)
            output_simulation_info(args.output_directory, args)
        except OSError:
            pass  # OK if already exists

    return args

def output_simulation_info(directory, args):
    filename = path.join(directory, 'info.txt')
    with open(filename, 'w') as f:
        f.write(str('Time Started: {0}\n'.format(time.strftime('%X %x %Z'))))
        for arg_name, arg_value in vars(args).items():
            f.write('{0}: {1}\n'.format(arg_name, str(arg_value)))

if __name__ == '__main__':
    main()
