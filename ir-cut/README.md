# IR CUT set

This little script uses python3 and rpi.GPIO to set the ir cut to
Night mode, or normal day mode (with the infrared filter enabled).

## Usage:
```
./camera-ircut.py --m night --g 16
```

Where `--m` sets the mode. Valid choices are `day` or `night`, and `--g` sets the GPIO port.
The default is 16 because I want it to.


To install the rpi.GPIO module, you need to do a `sudo apt install python3-rpi.gpio`
