#!/usr/bin/env python3

''' motortest.py '''

import motorsetup
from time import sleep

sm_mot,sm_axis,big_mot,big_axis = motorsetup.start()

'start TMCL programs on modules with correct speeds and number of cycles'

big_mot.move_absolute(0)
sm_mot.move_absolute(0)
sleep(2)

for i in range(4):
    big_mot.move_absolute(51200)
    sleep(3)
    sm_mot.move_absolute(12800)
    sleep(3)
    big_mot.move_absolute(-51200)
    sleep(3)
    sm_mot.move_absolute(-12800)
    sleep(3)

big_mot.move_absolute(0)
sm_mot.move_absolute(0)
