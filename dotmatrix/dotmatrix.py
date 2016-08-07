#!/usr/bin/env python
import RPi.GPIO as GPIO
import time, random
from dotmatrix_letters import *
SDI   = 11
RCLK  = 12
SRCLK = 13

# Value L: 1=pixel off, 0=pixel on
# Letters are at dotmatrix_letters.py file.
# Value H: As only one line can be sent at a time, this just draws from top to bottom, one by one
code_H = [0b00000001,0b00000010,0b00000100,0b00001000,0b00010000,0b00100000,0b01000000,0b10000000]

def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'

def setup():
	GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def hc595_in(dat):
	for bit in range(0, 8):
		GPIO.output(SDI, 0x80 & (dat << bit))
		#print "I am sending {:08b}".format(0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		#time.sleep(0.001)
		GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)

def display_letter(letter):
    for j in range(0,20):
        for i in range(0, len(code_H)):
            hc595_in(alphabet[letter][i])
            #print "L is {:08b}".format(alphabet[letter][i])
            hc595_in(code_H[i])
            hc595_out()

def display_phrase(phrase):
    while True:
        for letter in phrase:
            display_letter(letter.upper())

def destroy():   # When program ending, the function is executed.
	GPIO.cleanup()

if __name__ == '__main__':   # Program starting from here
    print_msg()
    setup()
    try:
        display_phrase("This is a test 0 0 0 ")
    except: # Always cleanup, not just with KeyboardInterrupt
		display_letter(" ")
		destroy()
