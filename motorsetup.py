#!/usr/bin/env python3

''' motorsetup.py '''
    
# create motor objects

from serial import Serial
import TMCL

def create (port_name, address, speed, accel, current, stand):
      
    port = Serial(port_name)
    bus = TMCL.connect(port)

    motor = bus.get_motor(address)
    axis = motor.axis

    axis.set(4, speed)
    axis.set(5, accel)
    axis.set(6, current)
    axis.set(7, stand)

    return motor, axis

def start ():
    sm_mot,sm_axis = create('/dev/ttyACM1',1,10240,5120,152,20)
    big_mot,big_axis = create('/dev/ttyACM0',1,1343,700,64,8)
    try:
        big_axis.set(153, 7)
        big_axis.set(154, 3)
    except:
        sm_mot,sm_axis = create('/dev/ttyACM0',1,10240,5120,152,20)
        big_mot,big_axis = create('/dev/ttyACM1',1,1343,700,64,8)
        big_axis.set(153, 7)
        big_axis.set(154, 3)
    return sm_mot,sm_axis,big_mot,big_axis
