#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time, os, pygame
import RPi.GPIO as GPIO
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont


# oled stuff
oled = ssd1306(port=1, address=0x3C)
font = ImageFont.truetype('redalert.ttf', 60)

GPIO.setmode(GPIO.BOARD) # Set pins by location
GPIO.setwarnings(False)

# Configure servo
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 100)
pwm.start(5)
global servoAngle

# Configure DC
MotorPin1   = 11    # pin11
MotorPin2   = 16    # pin12
MotorEnable = 13    # pin13
GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
GPIO.setup(MotorPin2, GPIO.OUT)
GPIO.setup(MotorEnable, GPIO.OUT)
GPIO.output(MotorEnable, GPIO.LOW) # motor stop

axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 0                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
interval = 0.00                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
os.environ["SDL_VIDEODRIVER"] = "dummy" # The idea is that it won't fail 
					# without X server - doesn't really 
					# work without sudo
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def printOled(message):
    with canvas(oled) as draw:
        draw.text((0, 0), message, font=font, fill=255)


# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            # Invert any axes which are incorrect
            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight
            # Determine Up / Down values
            if upDown < -0.1:
                moveUp = True
                moveDown = False
            elif upDown > 0.1:
                moveUp = False
                moveDown = True
            else:
                moveUp = False
                moveDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                moveLeft = True
                moveRight = False
            elif leftRight > 0.1:
                moveLeft = False
                moveRight = True
            else:
                moveLeft = False
                moveRight = False
servoAngle=12.0
increment=0.0
message="Hi! ", servoAngle
try:
    print 'Press [ESC] to quit'
    # Loop indefinitely
    while True:
	message=str(servoAngle)
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        servoAngle=servoAngle+increment
        if servoAngle <= 21.0 and servoAngle >= 2.0:
            pwm.ChangeDutyCycle( servoAngle )
        else:
            increment=0.0
        printOled(message)
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif moveLeft:
                if servoAngle < 21.0:
                    increment=1
                message="Left v="+str(servoAngle+increment)
            elif moveRight:
                if servoAngle > 2.0:
                    increment=-1
                message="Right v="+str(servoAngle+increment)
            elif moveUp:
                #servoAngle=12.0
                message="Up v="+str(servoAngle+increment)+"\nClockwise"
                GPIO.output(MotorEnable, GPIO.HIGH) # motor driver enable
		GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
		GPIO.output(MotorPin2, GPIO.LOW)
            elif moveDown:
                message="Down v="+str(servoAngle+increment)+"\nAnti-lockwise"
                GPIO.output(MotorEnable, GPIO.HIGH) # motor driver enable
		GPIO.output(MotorPin1, GPIO.LOW)   # anticlockwise
		GPIO.output(MotorPin2, GPIO.HIGH)
            else:
                increment=0.0
                message="Release. v="+str(servoAngle+increment)
                GPIO.output(MotorEnable, GPIO.LOW) # motor stop
        # Wait for the interval period
        time.sleep(interval)

    # Disable all drives
    #MorOff()
    GPIO.output(MotorEnable, GPIO.LOW) # motor stop

except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    print "Tchau"
    #MotorOff()
