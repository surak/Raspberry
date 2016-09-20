#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

MotorPin1   = 11    # pin11
MotorPin2   = 16    # pin12
MotorEnable = 13    # pin13

def setup():
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
	GPIO.setup(MotorPin2, GPIO.OUT)
	GPIO.setup(MotorEnable, GPIO.OUT)
	GPIO.output(MotorEnable, GPIO.LOW) # motor stop

def loop():
	while True:
		print 'Press Ctrl+C to end the program...'
		GPIO.output(MotorEnable, GPIO.HIGH) # motor driver enable
		GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
		GPIO.output(MotorPin2, GPIO.LOW)
		print "Clockwise"
		time.sleep(2)
		
		GPIO.output(MotorEnable, GPIO.LOW) # motor stop
		print "stop"
		time.sleep(1)
		
		GPIO.output(MotorEnable, GPIO.HIGH) # motor driver enable
		GPIO.output(MotorPin1, GPIO.LOW)   # anticlockwise
		GPIO.output(MotorPin2, GPIO.HIGH)
		print "Anticlockwise"
		time.sleep(2)
		
		GPIO.output(MotorEnable, GPIO.LOW) # motor stop
		print "Stop"
		time.sleep(1)

def destroy():
	GPIO.output(MotorEnable, GPIO.LOW) # motor stop
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

