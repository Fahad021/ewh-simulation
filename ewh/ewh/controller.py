from ewh import ElectricWaterHeater, make_heater
from states import OnState, PowerUsage

import logging
import pprint
import random
import uuid
import csv

class Controller(object):
    def __init__(self, heater, cid=None, randomize=False):
        self._usage_state_changes = 0
        self._commands_received = 0
        self._ewh = heater
        self._cid = cid
        self._usage_state = PowerUsage.REGULAR
        self._mapping = []

    def poll(self):
        """Update the EWH's temperature as if no message had been sent."""
        self._ewh.update()

    def receive_low_power_signal(self):
        """Simulate a command from the hub to go into low-power mode."""
        self._usage_state = PowerUsage.LOW
        self._ewh.go_to_low_power_mode()
        self._ewh.update()

    def receive_regular_power_signal(self):
        """Simulate a command from the hub to go into regular-power mode."""
        self._usage_state = PowerUsage.REGULAR
        self._ewh.go_to_regular_power_mode()
        self._ewh.update()

    def info(self, include_ewh=False):
        d = {
            'power_usage_state': str(self._usage_state),
            'id': str(self._cid),
        }

        if include_ewh:
            d['heater'] = self._ewh.info(include_config=True)

        return d

    def data_output(self):
        d = self._ewh.data_output()
        d['usage_state'] = 1 if self._usage_state == PowerUsage.LOW else 0
        return d

    def time_step_data():
        return self._mapping

def make_controller_and_heater(tank_size, env=None, cid=None, randomize=False):
    if cid is None:
        cid = uuid.uuid1()  # "random" identifier

    heater = make_heater(tank_size, env=env, hid=cid, randomize=randomize)
    return Controller(heater, cid=cid)

def output_controller_to_csv(control, csv_file):
    fieldnames = ('time_step', 'temperature', 'on_state', 'usage_state', 'demand', 'inlet', 'ambient')
    with open(csv_file, 'ab') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheaders()

        for ts, tsd in enumerate(control.time_step_data()):
            tsd['time_step'] = ts
            writer.writerow(tsd)
