import argparse
import os.path

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


    # TODO: output directory

    args = parser.parse_args()

    if args['csv_directory'] is None:
        args['csv_directory'] = '../Data/'

    if args['tank_size'] == 180:
        args['tank_size'] = TankSize.SMALL
    else:
        args['tank_size'] = TankSize.LARGE

    if args['population_size'] is None:
        args['population_size'] = 10000

    if not os.path.isdir(csv_directory):
        parser.error("Directory '{0}' does not exist.".format(csv_directory))

    return args

if __name__ == '__main__':
    main()
