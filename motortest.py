#!/usr/bin/env python3

''' motortest.py '''

import motorsetup
from time import sleep

# create motor and axis objects
sm_mot,sm_axis,big_mot,big_axis = motorsetup.start()

sm_mot.move_absolute(0)                 # move small motor to zero
big_mot.move_absolute(0)                # move big motor to zero
sleep(2)                                # wait

for i in range(4):                      # repeat four times
    sm_mot.move_absolute(12800)         # move small motor to 1/4 revolution
    sleep(2)                            # wait
    big_mot.move_absolute(51200)        # move big motor to 1/4 revolution
    sleep(2)                            # wait
    sm_mot.move_absolute(-12800)        # move small motor to -1/4 revolution
    sleep(2)                            # wait
    big_mot.move_absolute(-51200)       # move big motor to -1/4 revolution
    sleep(2)                            # wait

sm_mot.move_absolute(0)                 # move small motor to zero
big_mot.move_absolute(0)                # move big motor to zero

