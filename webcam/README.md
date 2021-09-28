# Time-lapse test

This takes pictures every time specified in crontab. Edit with `crontab -e`

For every minute, add this:

```
* * * * * ~/Devel/Raspberry/webcam/timelapse.sh 2>&1
```

In order to generate a timelapse, do this from the images directory:
```ffmpeg -r 12 -pattern_type glob -i '*.jpg' -s hd1080 -vcodec libx264 timelapse.mp4```
