import cwiid, time, pdb, serial

button_delay = 0.1

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
print 'Press the directional buttons to move around the robot'

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
    pdb.set_trace()
    return bytearray(pwm_array)


ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)    # replace serial port
ser.reset_input_buffer()

while True:
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
        if (buttons & cwiid.BTN_UP):
            print 'Going forward'
            pwm_message = construct_pwm_message(200, 0, 1, 0)
            ser.write(pwm_message)
            
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_DOWN):
            print 'Going backward'
            pwm_message = construct_pwm_message(200, 0, 0, 0)
            ser.write(pwm_message)
            time.sleep(button_delay)

        if (buttons & cwiid.BTN_LEFT):
            print 'Going Left'
            pwm_message = construct_pwm_message(0, 200, 0, 0)
            ser.write(pwm_message)
            time.sleep(button_delay)

        if(buttons & cwiid.BTN_RIGHT):
            print 'Going Right'
            pwm_message = construct_pwm_message(0, 200, 0, 1)
            ser.write(pwm_message)
            time.sleep(button_delay)
