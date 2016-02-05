# ewh-simulation
Simulation of a network of electric water heaters

## Setup

### Mac without Virtualenv

```bash
$ brew install python3
$ git clone git@github.com:ryanordille/ewh-simulation.git
$ cd ewh-simulation
$ pip3 install -r requirements.txt
```

### Mac with Virtualenv

```bash
$ brew install python3
$ pip3 install virtualenv
$ git clone git@github.com:ryanordille/ewh-simulation.git
$ cd ewh-simulation
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Running

(coming soon)

## Testing

```bash
$ python -m unittest tests
```
