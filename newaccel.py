# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Coded by The Raspberry Pi Guy. Work based on some of Matt Hawkins's!

import cwiid, time, pdb, serial

button_delay = 0.1
min_pwm = 50
steering_pwm_mag = 128
max_pwm = 255
steering_dir = None

last_msg_time = 0
msg_min_period = 100

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
    wii=cwiid.Wiimote()
except RuntimeError:
    print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
    quit()

print 'Wiimote connection established!\n'
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

time.sleep(3)

wii.rpt_mode = cwiid.RPT_BTN

state = "idle"

def construct_pwm_message(x_pwm, y_pwm, x_dir, y_dir):
    '''
    x is forward (1 forward 0 backward)
    y is side to side (1 right 0 left)

    Motor Numbering
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3
    '''
    direction = str(x_dir)*2 + str(y_dir)*2
    pwm_array = [x_pwm, x_pwm, y_pwm, y_pwm, int(direction, 2)]
    return pwm_array

def update_steering(drive_pwm, steering_pwm, steering_dir):
    pwm_message = construct_pwm_message(drive_pwm, steering_pwm_mag, 1, steering_dir)
    if time.time()-last_msg_time > msg_min_period:
        ser.write(pwm_message)
        last_msg_time = time.time()
        return True
    return False

# Future serial code
'''
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)    # replace serial port
ser.reset_input_buffer()
'''

while True:
    while state == "bowling":
        if (buttons & cwiid.BTN_A):
            print 'STOPPING ROBOT'
            drive_pwm = 0
            ser.write(construct_pwm_message(0,0,0,0))
            state = 'idle'
            time.sleep(button_delay)

        if(buttons & cwiid.BTN_2):
            print 'CHEATING MODE ACTIVATED'
            state = "steering"
            time.sleep(button_delay)

        wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        checks = 0
        holding = 1
        window_on = False
        max_in_window = 0
        while holding and checks < 20:
            acc = wii.state['acc']
            if acc[1] > 160:
                window_on = True
            if window_on:
                if max_in_window < acc[1]:
                    max_in_window = acc[1]
                checks+=1
            time.sleep(0.01)
            holding = (buttons & cwiid.BTN_B)
        if(checks == 20):
            speed_percent = float(max_in_window-160)/float(255-160)
            print("Motor speed:",speed_percent,"%")
            drive_pwm = int(min_pwm + speed_percent*(max_pwm-min_pwm))
            pwm_message = construct_pwm_message(drive_pwm, 0, 1, 0)
            # Future serial code
            ser.write(pwm_message)

    while state == "steering":
        buttons = wii.state['buttons']

        if (buttons & cwiid.BTN_A):
            print 'STOPPING ROBOT'
            drive_pwm = 0
            ser.write(construct_pwm_message(0,0,0,0))
            state = 'idle'
            time.sleep(button_delay)

        wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        acc = wii.state['acc']

        steering_percent = float(acc[1]-128) / float(35)
        if (abs(steering_percent) < 0.3):
            print 'straight!'
            continue
        if (abs(steering_percent) > 1):
            steering_percent = 1.0 if steering_percent>0 else -1.0
        if steering_percent > 0:
            print 'steering',steering_percent,'to the left'
            steering_dir = 0
        else:
            print 'steering',steering_percent*-1,'to the right'
            steering_dir = 1
        
        update_steering(drive_pwm, steering_pwm_mag, steering_dir)

    while state == "idle":
        buttons = wii.state['buttons']

        # Detects whether + and - are held down and if they are it quits the program
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
            print '\nClosing connection ...'
            # NOTE: This is how you RUMBLE the Wiimote
            wii.rumble = 1
            time.sleep(1)
            wii.rumble = 0
            exit(wii)

        # The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
        if (buttons & cwiid.BTN_LEFT):
            print 'Left pressed'
            time.sleep(button_delay)

        if(buttons & cwiid.BTN_RIGHT):
            print 'Right pressed'
            time.sleep(button_delay)

        if(buttons & cwiid.BTN_2):
            print 'CHEATING MODE ACTIVATED'
            state = "steering"
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_B):
            print 'Sensing acceleration. Bowl now!'
            state = "bowling"
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_MINUS):
            print 'Minus Button pressed'
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_PLUS):
            print 'Plus Button pressed'
            time.sleep(button_delay)
