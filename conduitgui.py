#!/usr/bin/env python3

''' conduitgui.py '''

# guizero documentation https://lawsie.github.io/guizero/
from guizero import App, Window, Box, Text, TextBox, Slider, PushButton, CheckBox, ButtonGroup
import motorsetup
from gpiozero import Button


sm_mot,sm_axis,big_mot,big_axis = motorsetup.start()                    # create motor and axis objects


def e_stop():                                                           
    sm_mot.send(128,0,0,0)                                              # stop motor applications
    big_mot.send(128,0,0,0)                            


def all_stop():
    reset()                                                             # call reset function
    sm_mot.stop()                                                       # stop motor movement
    big_mot.stop()


switch = Button(13)                                                     # create emergency stop switch object
switch.when_pressed = e_stop                                            # set up function to call when switched
switch.when_released = all_stop                                         # set up function to call when released


def two_motor():
    global sm_done,big_done,total
    sm_ready = sm_mot.get_user_var(7)                                   # get small motor user variable 7 (ready flag)
    if sm_ready == 1:                                                   # if small motor ready,
        big_mot.set_user_var(6,1)                                       # set big motor user variable 6 to one (done flag)
    big_ready = big_mot.get_user_var(7)                                 # get big motor user variable 7 (ready flag)
    if big_ready == 1:                                                  # if big motor ready,
        sm_mot.set_user_var(6,1)                                        # set small motor user variable 6 to one (done flag)
    sm_check = sm_mot.get_user_var(3)                                   # get small motor user variable 3 (cycles check)
    if sm_check >= total:                                               # if cycles check is greater than or equal to total test cycles,
        sm_mot.set_user_var(5,1)                                        # set small motor user variable 5 to one (finished flag)
        sm_done = True
    big_check = big_mot.get_user_var(3)                                 # get big motor user variable 3 (cycles check)
    if big_check >= total:                                              # if cycles check is greater than or equal to total test cycles,
        big_mot.set_user_var(5,1)                                       # set big motor user variable 5 to one (finished flag)
        big_done = True
    if sm_done and big_done == True:                                    # if both motors finished,                  
        sm_mot_on.enable()                                              # enable motor status checkboxes
        big_mot_on.enable()
        mot_activity()                                                  # call motor activity function
        reset_button.enable()                                           # enable reset button
        reset_button.bg = 'sky blue'
        start_button.enable()                                           # enable start button
        start_button.bg = 'green'
        stop_button.disable()                                           # disable stop button
        stop_button.bg = 'light salmon'
        run_text.hide()                                                 # hide test running text
        run_text.cancel(color)                                          # cancel scheduled call to test running text color function
        done_text.show()                                                # enable test finished text
        app.cancel(two_motor)                                           # cancel scheduled call to two-motor function
        sm_done = False
        big_done = False
        dual = False
    counter_text.value = 'Cycles completed: ' + str(big_check)          # update cycle counter text


def one_motor(motor,axis):
    global total
    check = motor.get_user_var(3)                                       # get user variable 3 (cycles check)
    if check >= total:                                                  # if cycles check is greater than or equal to total test cycles,
        motor.set_user_var(5,1)                                         # set user variable 5 to one (finished flag)
        sm_mot_on.enable()                                              # enable motor status checkboxes
        big_mot_on.enable()                                             
        mot_activity()                                                  # call motor activity function
        reset_button.enable()                                           # enable reset button
        reset_button.bg = 'sky blue'
        start_button.enable()                                           # enable start button
        start_button.bg = 'green'
        stop_button.disable()                                           # disable stop button
        stop_button.bg = 'light salmon'
        run_text.hide()                                                 # hide test running text
        run_text.cancel(color)                                          # cancel scheduled call to test running text color function
        done_text.show()                                                # show test finished text
        app.cancel(one_motor)                                           # cancel scheduled call to one-motor test function
        solo = False
    counter_text.value = 'Cycles completed: ' + str(check)              # update cycle counter text


def start():
    global solo,dual,sm_on,big_on,pause
    if pause == False:                                                  # if test is not paused,
        reset()                                                         # call reset function
        if sm_on == True and big_on == False:                           # if starting small motor test,
            sm_mot.send(129,0,0,0)                                      # start small motor application
            solo = True
            app.repeat(250,one_motor,[sm_mot,sm_axis])                  # schedule call to one-motor test function
        elif sm_on == False and big_on == True:                         # if starting big motor test,
            big_mot.send(129,0,0,0)                                     # start big motor application
            solo = True
            app.repeat(250,one_motor,[big_mot,big_axis])                # schedule call to one-motor test function
        else:                                                           # if starting two-motor test,
            sm_mot.send(129,0,0,0)                                      # start motor applications
            big_mot.send(129,0,0,0)
            dual = True
            app.repeat(150,two_motor)                                   # schedule call to two-motor test function
    elif pause == True:                                                 # if test is paused,
        if sm_on == True:                                               # if continuing small motor test,
            sm_mot.send(129,0,0,0)                                      # start small motor application
        if big_on == True:                                              # if continuing big motor test,
            big_mot.send(129,0,0,0)                                     # start big motor application
    sm_speed.disable()                                                  # disable all entries
    sm_start.disable()
    sm_end.disable()
    big_speed.disable()
    big_start.disable()
    big_end.disable()
    pattern.disable()
    cycles.disable()
    submit_button.disable()                                             # disable submit button
    submit_button.bg = 'light gray'
    reset_button.disable()                                              # disable reset button
    reset_button.bg = 'light gray'
    start_button.disable()                                              # disable start button
    start_button.bg = 'pale green'
    stop_button.enable()                                                # enable stop button
    stop_button.bg = 'red'
    run_text.show()                                                     # show test running text
    run_text.repeat(750,color)                                          # schedule call to test running text color function
    pause_text.hide()                                                   # hide test paused text
    pause = False                                                       
    done_text.hide()                                                    # hide test finished text


def stop():
    global pause                                              
    sm_mot.send(128,0,0,0)                                              # stop motors applications
    big_mot.send(128,0,0,0)
    sm_mot_on.enable()                                                  # enable motor status checkboxes
    big_mot_on.enable()
    mot_activity()                                                      # call motor activity function
    reset_button.enable()                                               # enable reset button
    reset_button.bg = 'sky blue'
    start_button.enable()                                               # enable start button
    start_button.bg = 'green'
    stop_button.disable()                                               # disable stop button
    stop_button.bg = 'light salmon'
    run_text.hide()                                                     # hide test running text
    run_text.cancel(color)                                              # cancel scheduled call to test running text color function
    pause_text.show()                                                   # show test paused text
    pause = True


def reset():
    global solo,dual,pause
    sm_mot.send(131,0,0,0)                                              # reset motor applications
    big_mot.send(131,0,0,0)
    sm_mot.move_absolute(0)                                             # move motors to zero
    big_mot.move_absolute(0)
    if solo == True:                                                    # if reseting one-motor test,
        app.cancel(one_motor)                                           # cancel scheduled call to one-motor test function
        solo = False
    elif dual == True:                                                  # if reseting two-motor test,
        app.cancel(two_motor)                                           # cancel scheduled call to two-motor test function
        dual = False
    for x in [3,5,6,7]:
        sm_mot.set_user_var(x,0)                                        # set user variables 3 and 5-7 to zero
        big_mot.set_user_var(x,0)
    counter_text.value = 'Cycles completed: 0'                          # reset cycle counter text to zero
    if pause == True:                                                   # if test is paused,
        start_button.enable()                                           # enable start button
        start_button.bg = 'green'
        pause_text.hide()                                               # hide test paused text
        pause = False
    done_text.hide()                                                    # hide test finished text


def submit():
    global sm_on,big_on,total,pause
    try:
        total = int(cycles.value)                                       # attempt to convert test cycles into integer
        if total <= 0:                                                  # if total test cycles is less than or equal to zero,
            app.error('Error','Invalid cycle entry')                    # display popup box with error icon
            return
    except:
        app.error('Error','Invalid cycle entry')                        # display popup box with error icon
        return
    if sm_mot_on.value == True and sm_dependent.value == False:         # if small motor checked and not dependent,
        try:
            smspeed = float(sm_speed.value)*853.33                      # attempt to convert small motor speed into float
            if smspeed <= 0:                                            # if small motor speed is less than or equal to zero,
                app.error('Error','Invalid speed entry')                # display popup box with error icon
                return
            sm_mot.set_user_var(0,int(smspeed))                         # set small motor user variable 0 to small motor speed
        except:
            app.error('Error','Invalid speed entry')                    # display popup box with error icon
            return
    if big_mot_on.value == True and big_dependent.value == False:       # if big motor checked and not dependent,
        try:
            bigspeed = float(big_speed.value)*111.848                   # attempt to convert big motor speed into float
            if bigspeed <= 0:                                           # if big motor speed is less than or equal to zero,
                app.error('Error','Invalid speed entry')                # display popup box with error icon
                return
            big_mot.set_user_var(0,int(bigspeed))                       # set big motor user variable 0 to big motor speed
        except:
            app.error('Error','Invalid speed entry')                    # display popup box with error icon
            return
    if sm_dependent.value == True:                                      # if small motor speed dependent,
        try:                                                            # attempt to calculate small motor speed
            smspeed = float(big_speed.value)*abs(sm_start.value-sm_end.value)/abs(big_start.value-big_end.value)
            sm_mot.set_user_var(0,int(smspeed*853.33))                  # set small motor user variable 0 to small motor speed
            sm_speed.value = str(round(smspeed,3))                      # update small motor speed input text
        except:
            app.error('Error','Invalid angle entry')                    # display popup box with error icon
            return
    elif big_dependent.value == True:                                   # if big motor speed dependent,
        try:                                                            # attempt to calculate big motor speed
            bigspeed = float(sm_speed.value)*abs(big_start.value-big_end.value)/abs(sm_start.value-sm_end.value)
            big_mot.set_user_var(0,int(bigspeed*111.848))               # set big motor user variable 0 to big motor speed
            big_speed.value = str(round(bigspeed,3))                    # update big motor speed input text
        except:
            app.error('Error','Invalid angle entry')                    # display popup box with error icon
            return
    if sm_mot_on.value == True:                                         # if small motor checked,
        sm_mot_active.show()                                            # show small motor status text
        sm_speed_text.value = 'Speed: ' + str(sm_speed.value)           # update small motor speed text
        sm_speed_text.show()                                            # show small motor speed text
        sm_start_text.value = 'Start angle: ' + str(sm_start.value)     # update small motor start angle text
        sm_start_text.show()                                            # show small motor start angle text
        sm_start_pos = -int(sm_start.value)*142.222                     # calculate small motor start position
        sm_mot.set_user_var(1,int(sm_start_pos))                        # set small motor user variable 1 to start position
        sm_end_text.value = 'End angle: ' + str(sm_end.value)           # update small motor end angle text
        sm_end_text.show()                                              # show small motor end angle text
        sm_end_pos = -int(sm_end.value)*142.222                         # calculate small motor end position
        sm_mot.set_user_var(2,int(sm_end_pos))                          # set small motor user variable 2 to end position
        sm_mot.set_user_var(4,0)                                        # set small motor user variable 4 to zero (no test pattern)
        sm_on = True
    else:                                                               # if small motor not checked,
        sm_mot_active.hide()                                            # hide all small motor text
        sm_speed_text.hide()                                            
        sm_start_text.hide()
        sm_end_text.hide()
        pattern_text.hide()                                             # hide test pattern text
        sm_on = False
    if big_mot_on.value == True:                                        # if big motor checked,
        big_mot_active.show()                                           # show big motor status text
        big_speed_text.value = 'Speed: ' + str(big_speed.value)         # update big motor speed text
        big_speed_text.show()                                           # show big motor speed text
        big_start_text.value = 'Start angle: ' + str(big_start.value)   # update big motor start angle text
        big_start_text.show()                                           # show big motor start angle text
        big_start_pos = int(big_start.value)*568.889                    # calculate big motor start position
        big_mot.set_user_var(1,int(big_start_pos))                      # set big motor user variable 1 to start position
        big_end_text.value = 'End angle: ' + str(big_end.value)         # update big motor end angle text
        big_end_text.show()                                             # show big motor end angle text
        big_end_pos = int(big_end.value)*568.889                        # calculate big motor end position
        big_mot.set_user_var(2,int(big_end_pos))                        # set big motor user variable 2 to end position
        big_mot.set_user_var(4,0)                                       # set big motor user variable 4 to zero (no test pattern)
        big_on = True
    else:                                                               # if big motor not checked,
        big_mot_active.hide()                                           # hide all big motor text
        big_speed_text.hide()
        big_start_text.hide()
        big_end_text.hide()
        pattern_text.hide()                                             # hide test pattern text
        big_on = False
    if sm_mot_on.value & big_mot_on.value == True:                      # if both motors checked,
        pattern_text.value = 'Test pattern: ' + str(pattern.value_text) # update test pattern text
        pattern_text.show()                                             # show test pattern text
        if pattern.value == 3:                                          # if test pattern is simultaneously
            sm_mot.set_user_var(4,3)                                    # set user variables 4 to three (simultaneous)
            big_mot.set_user_var(4,3)
        elif pattern.value == 2:                                        # if test pattern is big motor first
            sm_mot.set_user_var(4,2)                                    # set small motor user variable 4 to two (second)
            big_mot.set_user_var(4,1)                                   # set big motor user variable 4 to one (first)
        elif pattern.value == 1:                                        # if test pattern is small motor first
            sm_mot.set_user_var(4,1)                                    # set small motor user variable 4 to one (first)
            big_mot.set_user_var(4,2)                                   # set big motor user variable 4 to two (second)
    cycles_text.value = 'Total cycles: ' + str(cycles.value)            # update total test cycles text
    cycles_text.show()                                                  # show total test cycles text
    if pause == False:                                                  # if test is not paused,
        start_button.enable()                                           # enable start button
        start_button.bg = 'green'
        done_text.hide()                                                # hide test finished text
    elif pause == True:                                                 # if test is paused,
        reset()                                                         # call reset function


def mot_activity():
    if sm_mot_on.value & big_mot_on.value == True:                      # if both motors checked,
        sm_speed.enable()                                               # enable all inputs
        sm_dependent.enable()
        sm_start.enable()
        sm_end.enable()
        big_speed.enable()
        big_dependent.enable()
        big_start.enable()
        big_end.enable()
        pattern.enable()
        cycles.enable()
        sm_dependent.value = False                                      # uncheck motor speed dependent inputs
        big_dependent.value = False
        submit_button.enable()                                          # enable submit button
        submit_button.bg = 'light blue'
    elif sm_mot_on.value == True:                                       # if only small motor checked,
        sm_speed.enable()                                               # enable small motor inputs
        sm_start.enable()
        sm_end.enable()
        big_speed.disable()                                             # disable big motor inputs
        big_start.disable()
        big_end.disable()
        sm_dependent.disable()                                          # disable speed dependent inputs
        big_dependent.disable()
        sm_dependent.value = False                                      # uncheck motor speed dependent inputs
        big_dependent.value = False
        pattern.disable()                                               # disable test pattern input
        cycles.enable()                                                 # enable test cycles input
        submit_button.enable()                                          # enable submit button
        submit_button.bg = 'light blue'
    elif big_mot_on.value == True:                                      # if only big motor checked,
        sm_speed.disable()                                              # disable small motor inputs
        sm_start.disable()
        sm_end.disable()
        big_speed.enable()                                              # enable big motor inputs
        big_start.enable()
        big_end.enable()
        sm_dependent.disable()                                          # disable speed dependent inputs
        big_dependent.disable()
        sm_dependent.value = False                                      # uncheck motor speed dependent inputs
        big_dependent.value = False
        pattern.disable()                                               # disable test pattern input
        cycles.enable()                                                 # enable test cycles input
        submit_button.enable()                                          # enable submit button
        submit_button.bg = 'light blue'
    else:                                                               # if no motors checked,
        sm_speed.disable()                                              # disable all inputs
        sm_dependent.disable()
        sm_start.disable()
        sm_end.disable()
        big_speed.disable()
        big_dependent.disable()
        big_start.disable()
        big_end.disable()
        pattern.disable()
        cycles.disable()
        sm_dependent.value = False                                      # uncheck motor speed dependent inputs
        big_dependent.value = False
        submit_button.disable()                                         # disable submit button
        submit_button.bg = 'light gray'


def dependent(motor):
    if motor == 'small':                                                # if small motor speed dependent clicked,
        if sm_dependent.value == True:                                  # if small motor speed dependent,
            big_dependent.value = False                                 # uncheck big motor speed dependent input
            sm_speed.disable()                                          # disable small motor speed input
            big_speed.enable()                                          # enable big motor speed input
        elif sm_dependent.value == False:                               # if small motor speed not dependent,
            sm_speed.enable()                                           # enable small motor speed input
    elif motor == 'big':                                                # if big motor speed dependent clicked,
        if big_dependent.value == True:                                 # if big motor speed dependent,
            sm_dependent.value = False                                  # uncheck small motor speed dependent input
            big_speed.disable()                                         # disable big motor speed input
            sm_speed.enable()                                           # enable small motor speed input
        elif big_dependent.value == False:                              # if big motor speed not dependent,
            big_speed.enable()                                          # enable big motor speed input
        

def key(number):
    if str(app.tk.focus_get()) == str(cycles.tk):                       # check cursor location
        cycles.append(number)                                           # add number/decimal to test cycles textbox
    elif str(app.tk.focus_get()) == str(sm_speed.tk):
        sm_speed.append(number)                                         # add number/decimal to small motor speed textbox
    elif str(app.tk.focus_get()) == str(big_speed.tk):
        big_speed.append(number)                                        # add number/decimal to big motor speed textbox


def clear():
    if str(app.tk.focus_get()) == str(cycles.tk):                       # check cursor location
        cycles.clear()                                                  # clear test cycles textbox
    elif str(app.tk.focus_get()) == str(sm_speed.tk):
        sm_speed.clear()                                                # clear small motor speed textbox
    elif str(app.tk.focus_get()) == str(big_speed.tk):
        big_speed.clear()                                               # clear big motor speed textbox


def close():
    reset()                                                             # call reset function
    if app.yesno('Quit','Are you sure?'):                               # check if app quit was intentional
        app.destroy()                                                   


def color():                                            
    if run_text.text_color == 'pale green':                             # alternate color of test running text
        run_text.text_color = 'dark green'
    else:
        run_text.text_color = 'pale green'

    
app = App(title='Glenair Conduit Test',                                             # base app object of GUI
          bg='light blue', height='800', width='800')
app.when_closed = close                                                             # set up function to call when quitting app
solo = False                                                                        # running a one-motor test boolean
dual = False                                                                        # running a two-motor test boolean
sm_done = False                                                                     # small motor finished boolean
big_done = False                                                                    # big motor finished boolean


instruction_box = Box(app, width='fill', align='top')                               # box containing simple test instructions
instruction_1 = Text(instruction_box,                                               # parameter instruction text
                     text='Choose testing parameters and click submit.', height='2')
instruction_2 = Text(instruction_box,                                               # button instruction text
                     text='Use the buttons below to control testing.', height='2')


bottom_box = Box(app, width='fill', align='bottom')                                 # box containing cycle counter, testing buttons, & signature
counter_text = Text(bottom_box, text='Cycles completed: 0', height='2')             # cycle counter text                   
start_button = PushButton(bottom_box, command=start, text='Start test', width='9',  # start test button calls start function (initally disabled)
                           enabled=False) 
start_button.bg = 'pale green'                          
blank_1 = Text(bottom_box, size=-12)                                                # spacer
stop_button = PushButton(bottom_box, command=stop, text='Stop test', width='9',     # stop test button calls stop function (initally disabled)
                         enabled=False)     
stop_button.bg = 'light salmon'                         
blank_2 = Text(bottom_box, size=-12)                                                # spacer
reset_button = PushButton(bottom_box, command=reset, text='Reset test', width='9')  # reset test button calls reset function                     
reset_button.bg = 'sky blue'                            
signature_text = Text(bottom_box,                                                   # signature text
                      text='Created by Kylie Fernandez for Glenair Paso Robles (2019)', size=-12, height='2')


display_box = Box(app, width=200, height='fill', align='right')                     # box containing current test parameters, status, & keypad
display_title = Text(display_box, text='Current parameters:', height='2')           # display box title text
cycles_text = Text(display_box, text='Total cycles:', visible=False, size=-12)      # total test cycles text (initially hidden)
sm_mot_active = Text(display_box, text='Small motor active', visible=False,         # small motor status text (initially hidden)
                     height='2', size=-12)
sm_speed_text = Text(display_box, text='Speed:', visible=False, size=-12)           # small motor speed text (initially hidden)
sm_start_text = Text(display_box, text='Start angle:', visible=False, size=-12)     # small motor start angle text (initially hidden)
sm_end_text = Text(display_box, text='End angle:', visible=False, size=-12)         # small motor end angle text (initially hidden)
big_mot_active = Text(display_box, text='Big motor active', visible=False,          # big motor status text (initially hidden)
                      height='2', size=-12)
big_speed_text = Text(display_box, text='Speed:', visible=False, size=-12)          # big motor speed text (initially hidden)
big_start_text = Text(display_box, text='Start angle:', visible=False, size=-12)    # big motor start angle text (initially hidden)
big_end_text = Text(display_box, text='End angle:', visible=False, size=-12)        # big motor end angle text (initially hidden)
pattern_text = Text(display_box, text='Test pattern:', visible=False, height='2',   # test pattern text (initially hidden)
                    size=-12)
run_text = Text(display_box, text='TEST RUNNING', color='dark green', height='2',   # test running text (initially hidden)
                visible=False)
pause_text = Text(display_box, text='TEST PAUSED', height='2', visible=False)       # test paused text (initially hidden)
pause = False                                                                       # test paused boolean
done_text = Text(display_box, text='TEST FINISHED', height='2', visible=False)      # test finished text (initially hidden)
keypad_box = Box(display_box, layout='grid', align='bottom')                        # box containing keypad within display box
button1 = PushButton(keypad_box, text='1', grid=[0,0], command=key, args=[1])       # number 1 button calls key function
button1.bg = 'sky blue'
button2 = PushButton(keypad_box, text='2', grid=[1,0], command=key, args=[2])       # number 2 button calls key function
button2.bg = 'sky blue'
button3 = PushButton(keypad_box, text='3', grid=[2,0], command=key, args=[3])       # number 3 button calls key function
button3.bg = 'sky blue'
button4 = PushButton(keypad_box, text='4', grid=[0,1], command=key, args=[4])       # number 4 button calls key function
button4.bg = 'sky blue'
button5 = PushButton(keypad_box, text='5', grid=[1,1], command=key, args=[5])       # number 5 button calls key function
button5.bg = 'sky blue'
button6 = PushButton(keypad_box, text='6', grid=[2,1], command=key, args=[6])       # number 6 button calls key function
button6.bg = 'sky blue'
button7 = PushButton(keypad_box, text='7', grid=[0,2], command=key, args=[7])       # number 7 button calls key function
button7.bg = 'sky blue'
button8 = PushButton(keypad_box, text='8', grid=[1,2], command=key, args=[8])       # number 8 button calls key function
button8.bg = 'sky blue'
button9 = PushButton(keypad_box, text='9', grid=[2,2], command=key, args=[9])       # number 9 button calls key function
button9.bg = 'sky blue'
button0 = PushButton(keypad_box, text='0', grid=[0,3,2,1], padx=27, command=key,    # number 0 button calls key function
                     args=[0])
button0.bg = 'sky blue'
dec_button = PushButton(keypad_box, text='.', grid=[2,3], padx=12, command=key,     # decimal button calls key function
                        args=['.'])
dec_button.bg = 'sky blue'
clr_button = PushButton(keypad_box, text='Clear', grid=[0,4,3,1], pady=5,           # clear button calls clear function
                        command=clear)
clr_button.bg = 'sky blue'


select_box = Box(app, width='fill', align='top')                                    # box containing select parameters title
select_box.bg = 'sky blue'
select_title = Text(select_box, text='Select parameters:', height='2')              # select parameters title text


submit_box = Box(app, width='fill', align='bottom')                                 # box containing test pattern & cycles inputs & submit button
submit_box.bg = 'sky blue'
test_pattern = Text(submit_box, text='Test pattern:', height='2', size=-12)         # test pattern input text
pattern = ButtonGroup(submit_box,                                                   # test pattern button group input (initially disabled)
                      options=[['Simultaneous ','3'],['Small motor first ','1'],['Big motor first ','2']], horizontal=True, enabled=False)
total_cycles = Text(submit_box, text='Number of cycles:', height='2', size=-12)     # test cycles input text
cycles = TextBox(submit_box, text='0', enabled=False)                               # test cycles textbox input (initially disabled)
cycles.tk.config(justify='center')                                                  # access tkinter object to center text
total = 0                                                                           # total test cycles variable
blank_3 = Text(submit_box, size=-12)                                                # spacer
submit_button = PushButton(submit_box, command=submit, text='Submit', enabled=False)# submit parameters button calls submit function (initially disabled)
submit_button.bg = 'light gray'
blank_4 = Text(submit_box, size=-12)                                                # spacer


sm_mot_box = Box(app, height='fill', width='fill', align='left')                    # box containing small motor parameter inputs
sm_mot_box.bg = 'sky blue'
sm_mot_on = CheckBox(sm_mot_box, text='Small motor active ', command=mot_activity)  # small motor status checkbox input calls motor activity function
sm_on = False                                                                       # small motor status boolean
sm_mot_speed = Text(sm_mot_box, text='Speed [rpm]:', height='2', size=-12)          # small motor speed input text
sm_speed = TextBox(sm_mot_box, text='0', enabled=False)                             # small motor speed textbox input (initially disabled)
sm_speed.tk.config(justify='center')                                                # access tkinter object to center text
sm_dependent = CheckBox(sm_mot_box, text='Speed dependent', command=dependent,      # small motor speed dependent checkbox input (initially disabled)
                        args=['small'], enabled=False)          
sm_start_angle = Text(sm_mot_box, text='Start angle:', height='2', size=-12)        # small motor start angle input text
sm_start = Slider(sm_mot_box, start='0', end='360', width='fill', enabled=False)    # small motor start angle slider input (initially disabled)
sm_end_angle = Text(sm_mot_box, text='End angle:', height='2', size=-12)            # small motor end angle input text
sm_end = Slider(sm_mot_box, start='0', end='360', width='fill', enabled=False)      # small motor end angle slider input (initially disabled)

sm_current_lim_txt = Text(sm_mot_box, text='Current Limit (mA):', height='2', size=-12)
sm_current_mA = Slider(sm_mot_box, start='0', end='3500', width='fill', 
                       enabled=True)                                                 #255 is max rated current of driver (5.5A RMS for TMCM1180 (big motor), 6A for TMCM1260)
sm_current = int(sm_current_mA.value/1000/6*255)

big_mot_box = Box(app, height='fill', width='fill', align='right')                  # box containing big motor parameter inputs
big_mot_box.bg = 'sky blue'
big_mot_on = CheckBox(big_mot_box, text='Big motor active ', command=mot_activity)  # big motor status checkbox input calls motor activity function
big_on = False                                                                      # big motor status boolean
big_mot_speed = Text(big_mot_box, text='Speed [rpm]:', height='2', size=-12)        # big motor speed input text
big_speed = TextBox(big_mot_box, text='0', enabled=False)                           # big motor speed textbox input (initially disabled)
big_speed.tk.config(justify='center')                                               # access tkinter object to center text
big_dependent = CheckBox(big_mot_box, text='Speed dependent', command=dependent,    # big motor speed dependent checkbox input (initially disabled)
                         args=['big'], enabled=False)        
big_start_angle = Text(big_mot_box, text='Start angle:', height='2', size=-12)      # big motor start angle input text
big_start = Slider(big_mot_box, start='-110', end='110', width='fill',              # big motor start angle slider input (initally disabled)
                   enabled=False)                         
big_end_angle = Text(big_mot_box, text='End angle:', height='2', size=-12)          # big motor end angle input text
big_end = Slider(big_mot_box, start='-110', end='110', width='fill', enabled=False) # big motor end angle slider input (initially disabled)

big_current_lim_txt = Text(big_mot_box, text='Current Limit (mA):', height='2', size=-12)
big_current_mA = Slider(big_mot_box, start='0', end='2500', width='fill', 
                       enabled=True)                                                 # 255 is max rated current of driver (5.5A RMS for TMCM1180 (big motor), 6A for TMCM1260)
big_current = int(big_current_mA.value/1000/5.5*255)

app.display()                                                                       # method displaying app on the screen

