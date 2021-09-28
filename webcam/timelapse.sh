#!/bin/bash

# This should be on your crontab
# * * * * * ~/Devel/Raspberry/webcam/timelapse.sh 2>&1

# this should be in the /etc/modules for the pi noir infrared camera
# besides the raspian-config camera module enabled
## Raspi noir video4linux
#bcm2835-v4l2

# To generate a timelapse: 
# ffmpeg -r 12 -pattern_type glob -i '*.jpg' -s hd1080 -vcodec libx264 timelapse.mp4

DATE=$(date +"%Y-%m-%d_%H%M")
raspistill -awb auto -o $HOME/images/$DATE.jpg


