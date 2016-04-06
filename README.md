# ewh-simulation
Simulation of a network of electric water heaters

* McGill University, Department of Electrical Engineering
* ECSE 456 (Fall 2015) / ECSE 457 (Winter 2016) -- Design Project
* Paul Boulay de Touchet and Ryan Ordille
* Supervised by Professor Francois Bouffard

## Project setup (Mac)

```bash
$ cd /path/to/wherever/you/keep/github/stuff/
$ brew install python3
$ pip3 install virtualenv
$ git clone git@github.com:ryanordille/ewh-simulation.git
$ cd ewh-simulation
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Running

```bash
$ cd ewh/ewh
$ python main.py --help
```

For example, to run a simulation with:

* 1000 water heaters
* large water tanks
* polling once per minute (i.e. 60 timesteps per hour)
* hub collecting/sending messages every five timesteps/minutes
* start at midnight on the 5th day
* end at 11:59 on the 6th day
* reactivation period of 2 hours after the peaks

```bash
$ python main.py --tank-size 270 --population-size 1000 --start-time-step 7200 \
      --end-time-step 8639 --hub-interval 5 --scaling-factor 60 --reactivation_hours 2
```

To view logs:

```bash
$ tail -f simulation_log.log
```
