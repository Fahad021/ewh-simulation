# ewh-simulation
Simulation of a network of electric water heaters

## Mac Setup

### Github setup

In the terminal:

```
$ ssh-keygen
[just keep pressing enter until you can type in a new command]
$ cat ~/.ssh/id_rsa.pub | pbcopy
```

This will copy your public key to your clipboard automatically.

On Github, click on your avatar (top-right corner), then Settings -> SSH Keys -> New SSH Key. Paste into the "Key" field (don't bother with a title) and click "Add SSH Key".

### Project setup

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

### PyCharm setup

* Install and open PyCharm
* Open the `ewh-simulation` folder as a new project
* Pycharm -> Preferences -> "Project: ewh-simulation"
* Select the "3.4.3 virtualenv" interpreter and press OK

## Running

(coming soon)

## Testing

```bash
$ python -m unittest tests
```
