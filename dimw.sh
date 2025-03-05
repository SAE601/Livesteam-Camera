#!/bin/bash

VIDEO_SIZE="640x480"
VIDEO_STREAM="/dev/video0"

ffmpeg -f v4l2 -video_size $VIDEO_SIZE -t 0.5 -i $VIDEO_STREAM stream/dimw.mp4
rm stream/dimw.mp4