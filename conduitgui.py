#!/usr/bin/env python3

''' conduitgui.py '''

# guizero documentation https://lawsie.github.io/guizero/
from guizero import App, Window, Box, Text, TextBox, Slider, PushButton, CheckBox, ButtonGroup
import motorsetup
from time import sleep
from gpiozero import Button

sm_mot,sm_axis,big_mot,big_axis = motorsetup.start()                    # create motor and axis objects

switch = Button(13)                                                     # create emergency stop switch object

def e_stop():                                                           # send commands to stop motor applications
    sm_mot.send(128,0,0,0)                              
    big_mot.send(128,0,0,0)                            

def all_stop():                                                         # send commands to stop motor movement
    sm_mot.stop()                                             
    big_mot.stop()

switch.when_pressed = e_stop                                            # set up function to call when switched
switch.when_released = all_stop                                         # set up function to call when released

def two_motor():
    global total
    sm_ready = sm_mot.get_user_var(7)
    if sm_ready == 1:
        sm_mot.set_user_var(6,1)
    big_ready = big_mot.get_user_var(7)
    if big_ready == 1:
        big_mot.set_user_var(6,1)
    sm_check = sm_mot.get_user_var(3)
    if sm_check >= total:
        sm_mot.set_user_var(5,1)
    big_check = big_mot.get_user_var(3)
    if big_check >= total:
        big_mot.set_user_var(5,1)
    if sm_check or big_check >= total:
        mot_activity()
        sm_mot_on.enable()
        big_mot_on.enable()
        reset_button.enable()
        reset_button.bg = 'sky blue'
        start_button.enable()
        start_button.bg = 'green'
        stop_button.disable()
        stop_button.bg = 'light salmon'
        run_text.hide()
        run_text.cancel(color)
        done_text.enable()
        app.cancel(two_motor)
    counter_text.value = 'Cycles completed: ' + str(big_check)

def one_motor(motor,axis):
    global total
    check = motor.get_user_var(3)
    if check >= total:
        motor.set_user_var(5,1)
        mot_activity()
        sm_mot_on.enable()
        big_mot_on.enable()
        reset_button.enable()
        reset_button.bg = 'sky blue'
        start_button.enable()
        start_button.bg = 'green'
        stop_button.disable()
        stop_button.bg = 'light salmon'
        run_text.hide()
        run_text.cancel(color)
        done_text.show()
        app.cancel(one_motor)
    counter_text.value = 'Cycles completed: ' + str(check)    

def start():
    global solo, dual, sm_on, big_on
    if sm_on == True and big_on == False:
        sm_mot.send(129,0,0,0)
        solo = True
        sleep(0.5)
        app.repeat(150,one_motor,[sm_mot,sm_axis])
    elif sm_on == False and big_on == True:
        big_mot.send(129,0,0,0)
        solo = True
        sleep(0.5)
        app.repeat(150,one_motor,[big_mot,big_axis])
    else:
        sm_mot.send(129,0,0,0)
        big_mot.send(129,0,0,0)
        dual = True
        sleep(0.5)
        app.repeat(150,two_motor)
    pattern.disable()
    cycles.disable()
    submit_button.disable()
    submit_button.bg = 'light gray'
    sm_mot_box.disable() # fix
    big_mot_box.disable() # fix
    reset_button.disable()
    reset_button.bg = 'light gray'
    start_button.disable()
    start_button.bg = 'pale green'
    stop_button.enable()
    stop_button.bg = 'red'
    done_text.hide()
    run_text.show()
    run_text.repeat(750,color)
    pause_text.hide()

def stop():
    global solo,dual
    sm_mot.send(128,0,0,0)
    big_mot.send(128,0,0,0)
    sm_mot.stop()
    big_mot.stop()
    if solo == True:
        app.cancel(one_motor)
        solo = False
    elif dual == True:
        app.cancel(two_motor)
        dual = False
    mot_activity()
    sm_mot_on.enable()
    big_mot_on.enable()
    reset_button.enable()
    reset_button.bg = 'sky blue'
    start_button.enable()
    start_button.bg = 'green'
    stop_button.disable()
    stop_button.bg = 'light salmon'
    run_text.hide()
    run_text.cancel(color)
    pause_text.show()

def reset():
    sm_mot.send(131,0,0,0)
    big_mot.send(131,0,0,0)
    sm_mot.move_absolute(0)
    big_mot.move_absolute(0)
    pause_text.hide()
    done_text.hide()
    counter_text.value = 'Cycles completed: 0'

def submit():
    global sm_on,big_on,total
    try:
        total = int(cycles.value)
        if total <= 0:
            app.error('Error','Invalid cycle entry')
            return
    except:
        app.error('Error','Invalid cycle entry')
        return
    if big_mot_on.value == True:
        try:
            bigspeed = float(big_speed.value)*55.924
            if bigspeed <= 0:
                app.error('Error','Invalid speed entry')
                return
            big_mot.set_user_var(0,int(bigspeed))
        except:
            app.error('Error','Invalid speed entry')
            return
    if sm_mot_on.value == True:
        try:
            smspeed = float(sm_speed.value)*853.33
            if smspeed <= 0:
                app.error('Error','Invalid speed entry')
                return
            sm_mot.set_user_var(0,int(smspeed))
        except ValueError:
            app.error('Error','Invalid speed entry')
            return
        sm_mot_active.show()
        sm_speed_text.value = 'Speed: ' + str(sm_speed.value)
        sm_speed_text.show()
        sm_start_text.value = 'Start angle: ' + str(sm_start.value)
        sm_start_text.show()
        sm_start_pos = -int(sm_start.value)*142.222
        sm_mot.set_user_var(1,int(sm_start_pos))
        sm_end_text.value = 'End angle: ' + str(sm_end.value)
        sm_end_text.show()
        sm_end_pos = -int(sm_end.value)*142.222
        sm_mot.set_user_var(2,int(sm_end_pos))
        sm_mot.set_user_var(4,0)
        sm_on = True
    else:
        sm_mot_active.hide()
        sm_speed_text.hide()
        sm_start_text.hide()
        sm_end_text.hide()
        pattern_text.hide()
        sm_on = False
    if big_mot_on.value == True:
        big_mot_active.show()
        big_speed_text.value = 'Speed: ' + str(big_speed.value)
        big_speed_text.show()
        big_start_text.value = 'Start angle: ' + str(big_start.value)
        big_start_text.show()
        big_start_pos = int(big_start.value)*568.889
        big_mot.set_user_var(1,int(big_start_pos))
        big_end_text.value = 'End angle: ' + str(big_end.value)
        big_end_text.show()
        big_end_pos = int(big_end.value)*568.889
        big_mot.set_user_var(2,int(big_end_pos))
        big_mot.set_user_var(4,0)
        big_on = True
    else:
        big_mot_active.hide()
        big_speed_text.hide()
        big_start_text.hide()
        big_end_text.hide()
        pattern_text.hide()
        big_on = False
    if sm_mot_on.value & big_mot_on.value == True:
        pattern_text.value = 'Test pattern: ' + str(pattern.value_text) 
        pattern_text.show()
        if pattern.value == 3:
            sm_mot.set_user_var(4,3)
            big_mot.set_user_var(4,3)
        elif pattern.value == 2:
            sm_mot.set_user_var(4,2)
            big_mot.set_user_var(4,1)
        elif pattern.value == 1:
            sm_mot.set_user_var(4,1)
            big_mot.set_user_var(4,2)
    cycles_text.value = 'Total cycles: ' + str(cycles.value)
    cycles_text.show()
    start_button.enable()
    start_button.bg = 'green'

def mot_activity():
    if sm_mot_on.value & big_mot_on.value == True:
        sm_speed.enable()
        sm_start.enable()
        sm_end.enable()
        big_speed.enable()
        big_start.enable()
        big_end.enable()
        pattern.enable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    elif sm_mot_on.value == True:
        sm_speed.enable()
        sm_start.enable()
        sm_end.enable()
        big_speed.disable()
        big_start.disable()
        big_end.disable()
        pattern.disable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    elif big_mot_on.value == True:
        sm_speed.disable()
        sm_start.disable()
        sm_end.disable()
        big_speed.enable()
        big_start.enable()
        big_end.enable()
        pattern.disable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    else:
        sm_speed.disable()
        sm_start.disable()
        sm_end.disable()
        big_speed.disable()
        big_start.disable()
        big_end.disable()
        pattern.disable()
        cycles.disable()
        submit_button.disable()
        submit_button.bg = 'light gray'

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
    sm_mot.send(128,0,0,0)                                              # send commands to stop motor applications
    big_mot.send(128,0,0,0)
    sm_mot.stop()                                                       # send commands to stop motor movement
    big_mot.stop()
    if app.yesno('Quit','Are you sure?'):                               # double-check app quit was intentional
        app.destroy()

def color():                                            
    if run_text.text_color == 'pale green':                             # alternate color of test running status text
        run_text.text_color = 'dark green'
    else:
        run_text.text_color = 'pale green'

    
app = App(title='Glenair Conduit Test',                                             # base app object of GUI
          bg='light blue', height='800', width='800')
app.when_closed = close                                                             # set up function to call when quitting app
solo = False                                                                        # running a one-motor test boolean
dual = False                                                                        # running a two-motor test boolean


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
pattern_text = Text(display_box, text='Test pattern:', visible=False, height='2',   # two-motor test pattern text (initially hidden)
                    size=-12)
run_text = Text(display_box, text='TEST RUNNING', color='dark green', height='2',   # test running status text (initially hidden)
                visible=False)
pause_text = Text(display_box, text='TEST PAUSED', height='2', visible=False)       # test paused status text (initially hidden)
done_text = Text(display_box, text='TEST FINISHED', height='2', visible=False)      # test finished status text (initially hidden)
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
sm_start_angle = Text(sm_mot_box, text='Start angle:', height='2', size=-12)        # small motor start angle input text
sm_start = Slider(sm_mot_box, start='0', end='360', width='fill', enabled=False) # small motor start angle slider input (initially disabled)
sm_end_angle = Text(sm_mot_box, text='End angle:', height='2', size=-12)            # small motor end angle input text
sm_end = Slider(sm_mot_box, start='0', end='360', width='fill', enabled=False)   # small motor end angle slider input (initially disabled)


big_mot_box = Box(app, height='fill', width='fill', align='right')                  # box containing big motor parameter inputs
big_mot_box.bg = 'sky blue'
big_mot_on = CheckBox(big_mot_box, text='Big motor active ', command=mot_activity)  # big motor status checkbox input calls motor activity function
big_on = False                                                                      # big motor status boolean
big_mot_speed = Text(big_mot_box, text='Speed [rpm]:', height='2', size=-12)        # big motor speed input text
big_speed = TextBox(big_mot_box, text='0', enabled=False)                           # big motor speed textbox input (initially disabled)
big_speed.tk.config(justify='center')                                               # access tkinter object to center text
big_start_angle = Text(big_mot_box, text='Start angle:', height='2', size=-12)      # big motor start angle input text
big_start = Slider(big_mot_box, start='-110', end='110', width='fill', enabled=False) # big motor start angle slider input (initally disabled)                         
big_end_angle = Text(big_mot_box, text='End angle:', height='2', size=-12)          # big motor end angle input text
big_end = Slider(big_mot_box, start='-110', end='110', width='fill', enabled=False)   # big motor end angle slider input (initially disabled)
                       

app.display()                                                                       # method displaying app on the screen

