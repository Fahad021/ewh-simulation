import math
import config
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




# Energy use in one day = water heater power rating * hours "on" in a day (units kWh)
# Energy use in one year = sum of all days in the year (units kWh)
# Export to csv in a per hour basis


