# Ok, so I thought about this for a while and it's much more complex than I previously thought of.
# We need to know which EWH is which EWH, and keep track for each EWH it's temperature and it's operating mode.
# To keep track of this I'm thinking two 3D arrays which should be updated by the PDE, the hub and the temperature
# logic.
# Array 1 : [10,000] [365] [24]
# Array 2 : [10,000] [365] [24]
# Both arrays are the same size. Array 1 will keep track of temperature,
# Array 1 enables us to know the temperature at a certain hour of a certain day of a specific EWH
# Array 2 stores operating mode which we will use binary (1 = on, 0 = off) Note: I modified this later on, too narrow
# Array 2 enables us to know the operating mode at every hour of every day for each EWH
# Assuming we don't break this further into minutes (which would bring our size to 5,256,000,000) we keep
# everything in a per hour basis (87,600,000 size) (Moreau checks every 5 min).
# That said, you are the coding expert and you might know of a much smarter way but this is what I'm thinking.

# This is confusing the fuck out of me.

# Now for both bidirectional and Unidirectional we need to know the peak periods for each day,
# we probably want to keep it constant throughout the year so maybe from 6 am to 10 am and 4 pm to 8 pm, we can change
# these later but this is what Alain Moreau uses. We can store this in binary form in a 1D 24 size array,
# where 1 = peak therefore send all EWH's into low power mode and 0 = no peak therefore you should be instructed
# on how to get back to regular mode.
# When it's 1 simple, send everyone into low power mode and if internal temperature goes below the
# threshold go back to regular mode (this brings some problems which I talk about later).
# Now when the peak is over things get tricky, there are several cases.
# If it's unidirectional or bidirectional and there is no distribution function (or distribution function = 0 hours)
# turn everyone back on at once.
# If however we have a random distribution function we have several cases.
# In unidirectional simply do (10,000)/(hours set for distribution function * 60) since we have no clue
# if a certain EWH is in regular mode due to one way communication. Also need to have an error prevention due to
# rounding.
#
# ------------- IGNORE BELOW ---- # Ignore because doesn't make a difference, we don't have the info anyways....
#
# First we need to know how many are in low power mode (ie how many didn't go back on during the peak period),
# let's call them X. Let's call Y the number of EWH who had to turn back on. Obviously X+Y=10,000.
# Let's start with unidirectional, we have no clue of temperature so randomly assign
# X/(hours set for distribution function * 60) EWH's to turn back on every minute,
# and round the number up in that calculation so math.ceil (so we aren't turning on a fraction of a EWH,
# and set a condition when we an error occurs saying we went over the population
# since the rounding will make the number >X.
#
# ------------- IGNORE ABOVE ----
#
# For bidirectional we will follow something similar except instead of randomly turning back on we will get the
# X EWH's and put them in increasing temperature order. Then using same formula as above turn them back on per minute
# basis.
# If we want to go further than this in bidirectional I have a great idea, instead of turning them back on
# linearly let's turn them back on smoothly where we analyze the temperature quickly and turn on slowly at
# beginning (the coldest ones since they will be turned on for longer anyways) and then turn back on faster
# the warmer ones as they will be warmer inside and will remain on for a shorter period of time.
# I'm thinking this may avoid a bit of constructive building at the beginning, this might make a smoother transition.
# If we don't want to analyze on a per case basis I have in mind a way of getting a nice formula for a general case.
# We can try it later on if time permits and see results, if good Bouffard will win noble prize and we will be forever
# immortalized with all the fame as we have cured the world of climate change, if not we can still show it
# and say it's bad and then nobody losses their time trying it and Trump wins the elections, no big deal.

# Also I'm worried we didn't set up the states well enough. We need to know for each state on or off. Let me explain my
# point. The EWH has been instructed to be in low power mode (we can safely assume when in this mode it is ALWAYS off).
# If an EWH needs to go into regular mode due to a threshold violation it will immediately be turned on until
# internal temperature is above the upper threshold. Now something I don't think we have thought about is what happens
# then, does it stay on regular mode or is it sent back to low power mode. I think the answer should be it depends,
# let me clarify.

# ------------- IGNORE BELOW ---- # Ignore because doesn't make a difference, we don't have the info anyways....

# Let's assume unidirectional communication first, if the EWH is found in the position above, it should be kept in
# regular mode regardless if the others are still in low power mode (power peak is still on).

# ------------- IGNORE Above ----

# Now if we have a bidirectional setup, we should send back the EWH into lower power mode IFF the power peak is still
# going on (6AM-10AM & 4PM-8PM) && there is a random distribution function. If the peak is over or there is no random
# distribution function we should keep it in regular mode to avoid having it in the queue as it's already fairly warm.
# Now in regular mode we want to know if it is on or off. In low power mode we know it will always be off. Adding
# this information adds more information to array 2. In which the 3rd array will no longer be 0,1  but can be
# 1 = low power mode OFF
# 2 = regular power mode OFF
# 3 = regular power mode ON
# no need for low power mode ON as it should not exist

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

# RYAN, in ewh.py line 100-101, I think:
# if self.heater_is_on():
#            self._total_time_on += 1
# Should be,
# if self.heater_is_on():
#            self._total_time_on += 1 * TIME_SCALING_FACTOR
# This would accomodate a more real time, as if we do every 5 min we want to show time on to be 5 min and not 1 min
# Also, we might need to reset this to zero every hour, as it doesn't make sense to keep it growing over the year
# Over a simple fix would be to subtract times each time, I'll do this for now but let's keep that in mind

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


