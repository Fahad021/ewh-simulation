# TODO LOW POWER MODE MANAGEMENT
# TODO NO COMMUNICATION
# No instructions, this is normal behavior

# TODO Unidirectional
# When receive_low_power_signal message is sent
# Update change_usage_state
# Temperature violation will allow EWH to go back intro regular mode and heat up to desired TEMP

# TODO Bidirectional
# Same as unidirectional, EXCEPT that whenever an EWH needs to turn back on it needs to inform hub it's turning back on
# (we might want to know it's water usage and temperature as to know why it turned back on, having a percentage of EWH
# who stayed off won't be enough)
# Need to know on a per peak basis (per day and morning or evening peak), as well don't count EWH twice per peak if
# it happens

# ---------------------------------------------------------------------------------------------------------------------

# TODO PICK UP MANAGEMENT
# TODO NO COMMUNICATION
# Background: no communication is the current system, this system has no hub. We are implementing this to have a
# comparison with our unidirectional and bidirectional systems. EWH's are free to act, each time temperature goes below
# their predetermined deadband, turn back on until hotter than upper limit.
# Control Interest: none
# Data interest: avg power use per day and in cold/hot days

# TODO Unidirectional
# Background: Of interest to us is Hub communicating with EWH's, not viceversa (because we wouldn't be able to send
# low power mode message, out of scope making controller being able to read off grid information as idea is to have
# dumb controller and smart hub). Need to feed peak times
# Control interest: reactivation period and temperature deadband (only if we change the way they operate in the
# sense that they will heat up to a defined deadband above lower limit instead of desired temperature)
# Data interest: avg daily power use, comparison to no communication and normal grid (see how many
# MW's we can shave off)
# Pick up Management:
# 1.- Not controlled: ie everyone is turned back at once (should create new peak)
#   if receive_regular_power_signal received
#       all EWH's population change_usage_state(PowerUsage.REGULAR)
#
# 2.- Random spread (regardless of internal Temp as we don't have this data). Need to define time period
# (1 hr, 2 hr etc). Could be nice to use queue and simply pop each amount every time step
#   if receive_regular_power_signal received & random spread management (define time)
#       turn on population by EWH's order this way
#           for every time step starting immediately turn on this amount of EWH's per time step
#           math.ceil EWH population size /( period time in hrs * (60 / time step))
#           careful of error due to rounding, as rounding to next closest int will definitely make the population
#           larger than it really is if we work with fractions. So might want to add an if statement preventing this

# TODO Bidirectional
# Background: Now we have EWH <--> HUB communication. Need to feed peak times and need to track every EWH with all
# it's data. So for each EWH know temperature, operation mode, power consumption etc for EACH time step
# Control interest: Potentially implement a nonlinear prioritized function
# Data interest: Same as Unidirectional as well as knowing how many EWH's managed to remain on/off during power peak
# Pick up Management:
# 1.- Not controlled: ie everyone is turned back at once (should create new peak)
#   if receive_regular_power_signal received
#       all EWH's population change_usage_state(PowerUsage.REGULAR)
# This should give same data as unidirectional
#
# 2.- Prioritized Function: since bidirectional, when receive receive_regular_power_signal message, order in queue
# by increasing order all temperatures. Then same function as unidirectional. Only difference is this discriminates by
# water temperature.
# We should clarify if we recalculate and reorder the queue after each time step, maybe there is a strong demand for
# one EWH which makes it eligible to switch places to turn on quicker

# ---------------------------------------------------------------------------------------------------------------------

# TODO COLD LOAD PICKUP
# We need to assume the entire network has been disconnected for a while
# Therefore make internal EWH temperature a random distribution of temperatures between incoming water temperature
# at the day tested and the air temperature of day tested
# Now this only applies to Unidirectional and Bidirectional EWH's
# Now we need to find a smart and efficient way of bringing them slowly back to temperatures.
# to do this we will need to think about a couple of ways and implement them to see actual results