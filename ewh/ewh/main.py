import argparse
import os.path

import simulation
import environment

def main():
    csv_directory, seed = parse_args()

    environment.setup()
    sim = SimulationHub(rng_seed=seed)
    sim.build_random_population()
    sim.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="rng seed", type=int)
    parser.add_argument("--csv",
        dest="csv_directory",
        help="directory containing input csv data files",
        metavar="DIRECTORY")
    # TODO: output directory

    args = parser.parse_args()

    if args['csv_directory'] is None:
        csv_directory = '../Data/'
    else:
        csv_directory = args['csv_directory']

    if not os.path.isdir(csv_directory):
        parser.error("Directory '{0}' does not exist.".format(csv_directory))

    return csv_directory, seed

if __name__ == '__main__':
    main()
