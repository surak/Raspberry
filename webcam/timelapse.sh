#!/bin/bash

# This script depends on "fswebcam", in order to capture pictures. 
# the cronjob would be something like
# * * * * * ~/Devel/Raspberry/webcam/timelapse.sh 2>&1

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 640x480 ~/Devel/Raspberry/webcam/images/$DATE.jpg
