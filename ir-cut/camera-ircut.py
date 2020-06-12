#!/usr/bin/env python3
"""This little snippet changes the IR cut of Raspberry Pi's camera:
https://www.waveshare.com/wiki/RPi_IR-CUT_Camera

For it, you need

- Python3
- The `python3-rpi.gpio` package. Install with `sudo apt install python3-rpi.gpio`
"""


import argparse
import RPi.GPIO as GPIO

def parse_arguments():
    """Receives command line input"""
    parser = argparse.ArgumentParser(description='Sets the ir cut mode.')
    parser.add_argument('--g', metavar='GPIO', default=16, type=int,
                        help='Choose GPIO. I use 16, so this is the default.')
    parser.add_argument('--m', metavar='MODE', default="night",
                        help='Choose "day" or "night". .')
    return parser.parse_args()

def set_gpio(MODE, PORT):
    if MODE == "day":
       OUTPUT=GPIO.HIGH
       print("Day mode on port", PORT)
    else:
        OUTPUT=GPIO.LOW
        print("Night mode on port", PORT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(PORT, OUTPUT)



if __name__ == "__main__":
    args = parse_arguments()
    set_gpio(MODE=args.m, PORT=args.g)
