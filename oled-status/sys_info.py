#!/usr/bin/env python
# This is based on Richard Hull's example: https://github.com/rm-hull/ssd1306
# You need his library in order for this example to work.
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#

import os
import sys
import socket
if os.name != 'posix':
    sys.exit('platform not supported')
import psutil
import time

from datetime import datetime
from luma.oled.device import ssd1306, sh1106
from luma.core.render import canvas
from PIL import ImageDraw, ImageFont

# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
            % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def myip(iface):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    #print(s.getsockname()[0])
    return "%s: %s" % (iface, s.getsockname()[0])
    s.close()

def stats(oled):
    font = ImageFont.load_default()
    font2 = ImageFont.truetype('./c-and-c.ttf', 12)
    with canvas(oled) as draw:
        draw.text((0, 00), myip('wlan0'), font=font2, fill=255)
        draw.text((0, 14), mem_usage(), font=font2, fill=255)
        draw.text((0, 26), disk_usage('/'), font=font2, fill=255)
        draw.text((0, 38), network('wlan0'), font=font2, fill=255)
        draw.text((0, 50), cpu_usage(), font=font2, fill=255)

def main():
    oled = ssd1306(port=1, address=0x3C, rotate=2)
    while True:
        stats(oled)
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
