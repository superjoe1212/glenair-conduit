#!/usr/bin/env python3

''' motorsetup.py '''

# https://github.com/NativeDesign/python-tmcl
import TMCL
from serial import Serial

def create (port_name, address, speed, accel, current, stand):
    
    port = Serial(port_name)                                    # open serial port
    bus = TMCL.connect(port)                                    # create bus instance

    motor = bus.get_motor(address)                              # get motor object
    axis = motor.axis                                           # create axis object

    axis.set(4, speed)                                          # set maximum positioning speed
    axis.set(5, accel)                                          # set maximum acceleration
    axis.set(6, current)                                        # set maximum current
    axis.set(7, stand)                                          # set maximum standby current

    for x in range(0,8):                                            
        motor.set_user_var(x,0)                                 # set user variables 0-7 to zero

    return motor, axis

def start ():
    
    sm_mot,sm_axis = create('/dev/ttyACM1',1,10240,5120,152,20) # use create function for small motor and axis
    big_mot,big_axis = create('/dev/ttyACM0',1,1343,440,64,8)   # use create function for big motor and axis
    
    try:
        big_axis.set(153, 7)                                    # attempt to set ramp divisor
        big_axis.set(154, 3)                                    # attempt to set pulse divisor
        
    except:                                                     # retry with flipped ports if error occurs
        sm_mot,sm_axis = create('/dev/ttyACM0',1,10240,5120,152,20) 
        big_mot,big_axis = create('/dev/ttyACM1',1,1343,440,64,8)
        big_axis.set(153, 7)
        big_axis.set(154, 3)
        
    return sm_mot,sm_axis,big_mot,big_axis
