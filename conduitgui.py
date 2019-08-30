#!/usr/bin/env python3

''' guitest.py '''

from guizero import App, Window, Box, Text, TextBox, Slider, PushButton, CheckBox, ButtonGroup
import motorsetup
from time import sleep

sm_mot,sm_axis,big_mot,big_axis = motorsetup.start()

def two_motor():
    print('running two motor')

def one_motor(motor,axis):
    print('running one motor')

def start():
    global solo, dual, sm_on, big_on
    if sm_on == True and big_on == False:
        app.repeat(250,one_motor,[sm_mot,sm_axis])
        solo = True
    elif sm_on == False and big_on == True:
        app.repeat(250,one_motor,[big_mot,big_axis])
        solo = True
    else:
        app.repeat(250,two_motor)
        dual = True
    submit_box.disable()
    submit_button.bg = 'light gray'
    sm_mot_box.disable()
    big_mot_box.disable()
    reset_button.disable()
    reset_button.bg = 'light gray'
    start_button.disable()
    start_button.bg = 'pale green'
    stop_button.enable()
    stop_button.bg = 'red'
    run_text.show()
    run_text.repeat(750,color)
    pause_text.hide()

def stop():
    sm_mot.send(128,0,0,0)
    big_mot.send(128,0,0,0)
    sm_mot.stop()
    big_mot.stop()
    global solo,dual
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
    global counter
    counter = 0
    counter_text.value = 'Cycles completed: 0'

def submit():
    global sm_on,big_on
    if big_mot_on.value == True:
        try:
            big_mot.set_user_var(0,int(float(big_speed.value)))
        except ValueError:
            app.error('Error','Invalid entry')
            return
    if sm_mot_on.value == True:
        try:
            sm_mot.set_user_var(0,int(float(sm_speed.value)))
        except ValueError:
            app.error('Error','Invalid entry')
            return
        sm_mot_active.show()
        sm_speed_text.value = 'Speed: ' + str(sm_speed.value)
        sm_speed_text.show()
        sm_start_text.value = 'Start angle: ' + str(sm_start_angle.value)
        sm_start_text.show()
        sm_start_pos = int(sm_start_angle.value)*142.222
        sm_mot.set_user_var(1,int(sm_start_pos))
        sm_end_text.value = 'End angle: ' + str(sm_end_angle.value)
        sm_end_text.show()
        sm_end_pos = int(sm_end_angle.value)*142.222
        sm_mot.set_user_var(2,int(sm_end_pos))
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
        big_start_text.value = 'Start angle: ' + str(big_start_angle.value)
        big_start_text.show()
        big_start_pos = int(big_start_angle.value)*568.889
        big_mot.set_user_var(1,int(big_start_pos))
        big_end_text.value = 'End angle: ' + str(big_end_angle.value)
        big_end_text.show()
        big_end_pos = int(big_end_angle.value)*568.889
        big_mot.set_user_var(2,int(big_end_pos))
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
    cycles_text.value = 'Total cycles: ' + str(cycles.value)
    cycles_text.show()
    start_button.enable()
    start_button.bg = 'green'

def mot_activity():
    if sm_mot_on.value & big_mot_on.value == True:
        sm_speed.enable()
        sm_start_angle.enable()
        sm_end_angle.enable()
        big_speed.enable()
        big_start_angle.enable()
        big_end_angle.enable()
        pattern.enable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    elif sm_mot_on.value == True:
        sm_speed.enable()
        sm_start_angle.enable()
        sm_end_angle.enable()
        big_speed.disable()
        big_start_angle.disable()
        big_end_angle.disable()
        pattern.disable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    elif big_mot_on.value == True:
        sm_speed.disable()
        sm_start_angle.disable()
        sm_end_angle.disable()
        big_speed.enable()
        big_start_angle.enable()
        big_end_angle.enable()
        pattern.disable()
        cycles.enable()
        submit_button.enable()
        submit_button.bg = 'light blue'
    else:
        sm_speed.disable()
        sm_start_angle.disable()
        sm_end_angle.disable()
        big_speed.disable()
        big_start_angle.disable()
        big_end_angle.disable()
        pattern.disable()
        cycles.disable()
        submit_button.disable()
        submit_button.bg = 'light gray'

def key(number):
    if str(app.tk.focus_get()) == str(cycles.tk):
        cycles.append(number)
    elif str(app.tk.focus_get()) == str(sm_speed.tk):
        sm_speed.append(number)
    elif str(app.tk.focus_get()) == str(big_speed.tk):
        big_speed.append(number)

def clear():
    if str(app.tk.focus_get()) == str(cycles.tk):
        cycles.clear()
    elif str(app.tk.focus_get()) == str(sm_speed.tk):
        sm_speed.clear()
    elif str(app.tk.focus_get()) == str(big_speed.tk):
        big_speed.clear()

def close():
    sm_mot.stop()
    big_mot.stop()
    if app.yesno('Quit','Are you sure?'):
        app.destroy()

def color():
    if run_text.text_color == 'pale green':
        run_text.text_color = 'dark green'
    else:
        run_text.text_color = 'pale green'
    
app = App(title='Glenair Conduit Test', bg='light blue', height='800', width='800')
app.when_closed = close
solo = False
dual = False

instruction_box = Box(app, width='fill', align='top')
instruction_1 = Text(instruction_box, text='Select testing parameters and click submit.', height='2')
instruction_2 = Text(instruction_box, text='Use the buttons below to control testing.', height='2')

bottom_box = Box(app, width='fill', align='bottom')
counter_text = Text(bottom_box, text='Cycles completed: 0', height='2')
counter = 0
start_button = PushButton(bottom_box, command=start, text='Start test', width='9', enabled=False)
start_button.bg = 'pale green'
blank_1 = Text(bottom_box, size=-12)
stop_button = PushButton(bottom_box, command=stop, text='Stop test', width='9', enabled=False)
stop_button.bg = 'light salmon'
blank_2 = Text(bottom_box, size=-12)
reset_button = PushButton(bottom_box, command=reset, text='Reset test', width='9')
reset_button.bg = 'sky blue'
signature = Text(bottom_box, text='Created by Kylie Fernandez for Glenair Paso Robles (2019)',
                 size=-12, height='2')

display_box = Box(app, width=200, height='fill', align='right')
display_title = Text(display_box, text='Current parameters:', height='2')
cycles_text = Text(display_box, text='Total cycles:', visible=False, size=-12)
sm_mot_active = Text(display_box, text='Small motor active', visible=False, height='2', size=-12)
sm_speed_text = Text(display_box, text='Speed:', visible=False, size=-12)
sm_start_text = Text(display_box, text='Start angle:', visible=False, size=-12)
sm_end_text = Text(display_box, text='End angle:', visible=False, size=-12)
big_mot_active = Text(display_box, text='Big motor active', visible=False, height='2', size=-12)
big_speed_text = Text(display_box, text='Speed:', visible=False, size=-12)
big_start_text = Text(display_box, text='Start angle:', visible=False, size=-12)
big_end_text = Text(display_box, text='End angle:', visible=False, size=-12)
pattern_text = Text(display_box, text='Test pattern:', visible=False, height='2', size=-12)
run_text = Text(display_box, text='TEST RUNNING', color='dark green', height='2', visible=False)
pause_text = Text(display_box, text='TEST PAUSED', height='2', visible=False)
key_box = Box(display_box, layout='grid', align='bottom')
button1 = PushButton(key_box, text='1', grid=[0,0], command=key, args=[1])
button1.bg = 'sky blue'
button2 = PushButton(key_box, text='2', grid=[1,0], command=key, args=[2])
button2.bg = 'sky blue'
button3 = PushButton(key_box, text='3', grid=[2,0], command=key, args=[3])
button3.bg = 'sky blue'
button4 = PushButton(key_box, text='4', grid=[0,1], command=key, args=[4])
button4.bg = 'sky blue'
button5 = PushButton(key_box, text='5', grid=[1,1], command=key, args=[5])
button5.bg = 'sky blue'
button6 = PushButton(key_box, text='6', grid=[2,1], command=key, args=[6])
button6.bg = 'sky blue'
button7 = PushButton(key_box, text='7', grid=[0,2], command=key, args=[7])
button7.bg = 'sky blue'
button8 = PushButton(key_box, text='8', grid=[1,2], command=key, args=[8])
button8.bg = 'sky blue'
button9 = PushButton(key_box, text='9', grid=[2,2], command=key, args=[9])
button9.bg = 'sky blue'
button0 = PushButton(key_box, text='0', grid=[0,3,2,1], padx=27, command=key, args=[0])
button0.bg = 'sky blue'
dec_button = PushButton(key_box, text='.', grid=[2,3], padx=12, command=key, args=['.'])
dec_button.bg = 'sky blue'
clr_button = PushButton(key_box, text='Clear', grid=[0,4,3,1], pady=5, command=clear)
clr_button.bg = 'sky blue'

select_box = Box(app, width='fill', align='top')
select_box.bg = 'sky blue'
select_title = Text(select_box, text='Choose parameters:', height='2')

submit_box = Box(app, width='fill', align='bottom')
submit_box.bg = 'sky blue'
test_pattern = Text(submit_box, text='Test pattern:', height='2', size=-12)
pattern = ButtonGroup(submit_box, options=[['Simultaneous ','0'],['Small motor first ','1'],
                                           ['Big motor first ','2']], horizontal=True, enabled=False)
cycles_total = Text(submit_box, text='Number of cycles:', height='2', size=-12)
cycles = TextBox(submit_box, text='0', enabled=False)
cycles.tk.config(justify='center')
blank_3 = Text(submit_box, size=-12)
submit_button = PushButton(submit_box, command=submit, text='Submit', enabled=False)
submit_button.bg = 'light gray'
blank_4 = Text(submit_box, size=-12)

sm_mot_box = Box(app, height='fill', width='fill', align='left')
sm_mot_box.bg = 'sky blue'
sm_mot_on = CheckBox(sm_mot_box, text='Small motor active ', command=mot_activity)
sm_on = False
sm_mot_speed = Text(sm_mot_box, text='Speed [rev/s]:', height='2', size=-12)
sm_speed = TextBox(sm_mot_box, text='0', enabled=False)
sm_speed.tk.config(justify='center')
sm_start = Text(sm_mot_box, text='Start angle:', height='2', size=-12)
sm_start_angle = Slider(sm_mot_box, start='-360', end='360', width='fill', enabled=False)
sm_end = Text(sm_mot_box, text='End angle:', height='2', size=-12)
sm_end_angle = Slider(sm_mot_box, start='-360', end='360', width='fill', enabled=False)

big_mot_box = Box(app, height='fill', width='fill', align='right')
big_mot_box.bg = 'sky blue'
big_mot_on = CheckBox(big_mot_box, text='Big motor active ', command=mot_activity)
big_on = False
big_mot_speed = Text(big_mot_box, text='Speed [rev/s]:', height='2', size=-12)
big_speed = TextBox(big_mot_box, text='0', enabled=False)
big_speed.tk.config(justify='center')
big_start = Text(big_mot_box, text='Start angle:', height='2', size=-12)
big_start_angle = Slider(big_mot_box, start='-90', end='90', width='fill', enabled=False)
big_end = Text(big_mot_box, text='End angle:', height='2', size=-12)
big_end_angle = Slider(big_mot_box, start='-90', end='90', width='fill', enabled=False)

app.display()
