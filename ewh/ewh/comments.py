# TODO PAUL communication protocol
# Tell entire population to go into low power mode
#   control.go_to_low_power()
# for i in range(0, 9999):
    # for j = current day:
        # for k = current hour:
#           EWH_mode[i,j,k] = 1
            # note set ALL ewh to low power mode regardless of temperature, next time they calculate those
            # with low temperature will turn back on

# Tell population to turn back on
#   right before count how many are in low power still
#   this could be some useful data, as in 75% didn't have to turn back on with our software
#   A better method would be to count only those who never turned back on, as those who turn back on but finish
#   warming up before the lowpower instructions and therefore go back to low power
#   control.go_to_regular_power()
#   update EWH_mode
# for i in range(0, 9999):
    # for j = current day:
        # for k = current hour:
#            if EWH_temperature[i,j,k] > REGULAR_POWER_LOWER_LIMIT:
#            EWH_mode[i,j,k] = 2
#            else:
#            EWH_mode[i,j,k] = 3
# I'm

# TODO Cases of turning back on
# Different methods, if all at same time or slowly (prioritized distribution function)

# If unidirectional, everyone gets turned back on at same time (all 10,000) regardless of Temperature

# If it's  bidirectional and there is no distribution function (or distribution function = 0 hours)
# turn everyone back on at once as well, only those that don't satisfy
# if EWH_temperature[i,j,k] > REGULAR_POWER_LOWER_LIMIT:

# If however we have a random distribution function we have several cases.
# In unidirectional simply do (10,000)/(hours set for distribution function * 60) since we have no clue
# if a certain EWH is in regular mode due to one way communication. Also need to have an error prevention due to
# rounding.

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

# Now if we have a bidirectional setup, we should send back the EWH into lower power mode IFF the power peak is still
# going on (6AM-10AM & 4PM-8PM) && there is a random distribution function. If the peak is over or there is no random
# distribution function we should keep it in regular mode to avoid having it in the queue as it's already fairly warm.
# Now in regular mode we want to know if it is on or off. In low power mode we know it will always be off. Adding
# this information adds more information to array 2. In which the 3rd array will no longer be 0,1  but can be
# 1 = low power mode OFF
# 2 = regular power mode OFF
# 3 = regular power mode ON
# no need for low power mode ON as it should not exist
