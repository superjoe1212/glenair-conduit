#!/usr/bin/env python3

''' switches.py '''

# module to check for button presses in the background

from gpiozero import Button
from time import sleep
from os import system
from signal import pause

power = Button (12)                 # create on/off switch object

def turn_off ():                    # shut down the raspberry pi
    sleep (1)
    system ('sudo shutdown -h now')

power.when_released = turn_off      # set up function to call when released

pause ()                            # wait for switch signal
