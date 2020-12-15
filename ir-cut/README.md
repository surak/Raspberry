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


# Day mode
![Day mode](https://github.com/surak/Raspberry/blob/master/ir-cut/ir-cut.jpg)

# Night mode
![Day mode](https://github.com/surak/Raspberry/blob/master/ir-cut/with-ir.jpg)

This code was made for my birdwatcher:

![Raspberry pi with camera and cd](https://github.com/surak/Raspberry/blob/master/ir-cut/IMG_8413.jpeg)
![Raspberry pi](https://github.com/surak/Raspberry/blob/master/ir-cut/IMG_8414.jpeg)

Add this to the crontab to turn daylight filter mode at 5am, and night mode at 22 to your crontab with `crontab -e`:

```
MAILTO=""
0 5 * * *  /home/pi/Devel/Raspberry/ir-cut/camera-ircut.py -m day
0 22 * * *  /home/pi/Devel/Raspberry/ir-cut/camera-ircut.py -m night
```
