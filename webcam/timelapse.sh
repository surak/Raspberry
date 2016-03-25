#!/bin/bash

# This script depends on "fswebcam", in order to capture pictures. 
# To convert them into a video, the package is "libav-tools"
# the cronjob would be something like
# * * * * * ~/Devel/Raspberry/webcam/timelapse.sh 2>&1
# avconv -f image2 -i foo-%03d.jpeg -r 12 -s WxH foo.avi
# mencoder is out, the other tool is out. avconv is in

# this should be in the /etc/modules for the pi noir infrared camera
# besides the raspian-config camera module enabled
## Raspi noir video4linux
#bcm2835-v4l2


DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam --fps 15 -S 8 -r 640x480 ~/Devel/Raspberry/webcam/images/$DATE.jpg
