#!/usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)
#pwm.ChangeDutyCycle( 90.0/10+2.5 )


#for i in range(0,180):
#   time.sleep(0.2)
#   pwm.ChangeDutyCycle(i/10.0+2.5)
#   print i
 
while True:
   pwm.ChangeDutyCycle( 0/10+2.5 )
   print "Zero degrees"
   time.sleep(1)

   pwm.ChangeDutyCycle( 45/10+2.5 )
   print "45 degrees"
   time.sleep(1)

   pwm.ChangeDutyCycle( 60/10+2.5 )
   print "60 degrees"
   time.sleep(1)

   pwm.ChangeDutyCycle( 90/10+2.5 )
   print "90 degrees"
   time.sleep(1)

   pwm.ChangeDutyCycle( 120/10+2.5 )
   print "120 degrees"
   time.sleep(1)
   
   pwm.ChangeDutyCycle( 150/10+2.5 )
   print "150 degrees"
   time.sleep(1)

   pwm.ChangeDutyCycle( 180/10+2.5 )
   print "180 degrees"
