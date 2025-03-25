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

    for x in range(8):                                            
        motor.set_user_var(x,0)                                 # set user variables 0-7 to zero (note these are different from axis parameters which were set previously)

    return motor, axis




def start ():
    i = 0
    i = findPort(i)
    sm_mot,sm_axis = create(str('/dev/ttyACM' + str(i)),1,10240,5000,135,20) # use create function for small motor and axis
    j = i+1
    j = findPort(j)
    big_mot,big_axis = create(str('/dev/ttyACM' + str(j)),1,1343,440,64,8)   # use create function for big motor and axis
            
    try:
        big_axis.set(153, 7)                                    # attempt to set ramp divisor
        big_axis.set(154, 3)                                    # attempt to set pulse divisor
        print('small motor port = ', i)
        print('big motor port = ', j)
        
    except:                                                     # retry with flipped ports if error occurs

        
        sm_mot,sm_axis = create(str('/dev/ttyACM' + str(j)),1,10240,5000,135,20) #max speed divided by 256microsteps * 200steps -> 12rpm for 10240
        big_mot,big_axis = create(str('/dev/ttyACM' + str(i)),1,1343,440,64,8)   #1343 max speed, with pulse divisor 3 = 48 rpm - max speed value is 2047
        big_axis.set(153, 7)
        big_axis.set(154, 3)
        print('small motor port = ', j, 'j variable')
        print('big motor port = ', i, 'i variable')        
        
    return sm_mot,sm_axis,big_mot,big_axis

def findPort(i):
    try:
        motor,axis = create(str('/dev/ttyACM' + str(i)),1,1343,440,64,8)
        print('success finding port ', i)
#        print(motor)
    except:
#        print('could not find port ',i)
        i = i + 1
        if i > 9:
            print('could not find port')
        else:
            findPort(i)
    return i


