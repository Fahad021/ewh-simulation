# ---------- PSEUDOCODE FOR POWER CONSUMPTION
import csv
import numpy as np
# Make several 10,000 by 365 by 24 arrays
EWH_temperature = np.zeros((10000,365,24)) # store temperature at every hour, every day, each EWH
EWH_mode = np.zeros((10000,365,24)) # store mode (1= low power and off, 2 = regular and off, 3 = regular and on
#  at every hour, every day, each EWH
EWH_time_on = np.zeros((10000,365,24)) # store minutes on per hour at every hour, every day, each EWH
EWH_energy_use_hour = np.zeros((10000,365,24)) # store energy use at every hour, every day, each EWH
EWH_energy_use_day = np.zeros((10000,365)) # store energy use per day
# EWH_time_on will store the number of minutes the EWH is on every hour (so "number of minutes on"/60), because
# the energy calculation requires amount of hours, so if on half hour multiplication will be times 0.5

# Now for actualizing temperatures, we want to perform this at every TIME_SCALING_FACTOR
# This will throw many errors, one at time zero since there is no data before time starts and this needs the data at
# previous time, and another error at the end of every day since at hour 00:00 of each new day there is no previous
# data, need to look into previous day at time 23:00
for i in range(0, 9999):
    for j in range(0, 365):
        for k in range(0, 24):
            if j == 0 and k == 0:
                # day 1, hour 1 case. Need to set initial values for all 10,000 ewh
                EWH_temperature[i,j,k] = #whatever we initially set initial temperature to
            elif k == 0:
                EWH_temperature[i,j,k] = new_temperature(self, EWH_temperature[i,j-1,23], demand)
                # this should take care of every midnight
            else:
            EWH_temperature[i,j,k] = new_temperature(self, EWH_temperature[i,j,k-1], demand)
            if EWH_temperature[i,j,k] < REGULAR_POWER_LOWER_LIMIT:
                if self._usage_state == PowerUsage.REGULAR:
                EWH_mode [i,j,k] = 3
                # need to turn back on as below temperature threshold for regular power config
                elif self._usage_state == PowerUsage.low:
                    if EWH_temperature[i,j,k] > LOW_POWER_LOWER_LIMIT:
                        EWH_mode [i,j,k] = 1
                        # stay off as peak period is on
                    elif EWH_temperature[i,j,k] < LOW_POWER_LOWER_LIMIT:
                        EWH_mode [i,j,k] = 3
                        # need to turn back on as below temperature threshold for low power config
            else:
                EWH_mode [i,j,k] = 2



# What I'm trying to do here is iterate through every EWH, every day and every hour. At each hour multiply
# times the power rating and store in the same EWH, same day, same hour the kWh value
for i in range(0, 9999):
    for j in range(0, 365):
        for k in range(0, 24):
            EWH_energy_use_hour.insert[i,j,k]= self._heating_element_rating * EWH_time_on.index[i,j,k]

# Here I want to sum all hours in a day and store in EWH_energy_use_day
for i in range(0, 9999):
    for j in range(0, 365):
        for k in range(0, 24):
            EWH_energy_use_day.insert[i,j,k] = EWH_energy_use_day.insert[i,j,k] + EWH_energy_use_hour.insert[i,j,k]

# write all info into CSV, manually (excel/matlab) dealing with so much data could result to be painful
# Regardless, I think the best way to store this in the CSV is in rows the ewh and column hours and days, but it will
# be huge. Not sure we want something so big. The info we want from a per hour basis is interesting to us but not for
# every day of the year. If we can extract only couple of days it would satisfy our needs and be so much less
# cumbersome

with open('../Data/Energy_Use_hour.csv', 'wb') as csvfile:
    for i in range(0, 9999):
        for j in range(45, 46): # this day should be around middle of February, would be good to show response in
            # cold weather conditions, we can then change the day as we want
            for k in range(0, 24):
            writer = csv.writer(csvfile)
            writer.writerows(EWH_energy_use_hour)

with open('../Data/Energy_Use_day.csv', 'wb') as csvfile:
    for i in range(0, 9999):
        for j in range(0, 365):
        writer = csv.writer(csvfile)
        writer.writerows(day)

#in the __init__() method, create a new instance variable as an empty array (something like self._temperature_list = []),
# then in the poll method add to that list (do self._temperature_list.append(temperature))

#the list will then be the temperature at that timestep (where the value of the list at the index
#  i will be the temperature at timestep i)

#and then when we collect the values in the simulation runner we'll convert that from timesteps into minutes/hours/days
# according to the time scaling factor

#at least that's how I'd do it


