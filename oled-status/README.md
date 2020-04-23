# Status Screen
This is just a status screen using the excellent library from Richard Hull's SSD1306 library, https://github.com/rm-hull/ssd1306.git , which in itself is already based on AdaFruit's one at https://github.com/adafruit/Adafruit_Python_SSD1306 

I've tested this on two screens: one, fully monochrome, and another with an yellow top area and a lower blue area. 

The colored one looks better, but has a missing line of pixels between yellow and blue. I bought here: https://www.aliexpress.com/item/Free-shipping-Yellow-blue-double-color-128X64-OLED-LCD-LED-Display-Module-For-Arduino-0-96/32233300972.html

The black and white one is exactly 128x64 and it's cheaper: https://www.aliexpress.com/item/Free-shipping-White-Yellow-blue-double-color-128X64-OLED-LCD-LED-Display-Module-For-Arduino-0/32233334632.html

To install, first install the oled library:

'''
sudo apt-get install python3-dev libfreetype6-dev libjpeg-dev build-essential python3-psutil python3-pip python3-pillow libopenjp2-7-dev
sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.oled
'''

Then, add this to `/etc/rc.local`:

`python3 [repo]/Raspberry/oled-status/sys_info.py &`
