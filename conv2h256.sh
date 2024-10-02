#!/bin/bash

inpfile="$1"
ffmpeg -i "$inpfile" -c:v libx265 "$inpfile".265.mp4
