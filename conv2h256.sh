#!/bin/bash

inpfile="$1"

flnBase=$(basename "$inpfile" .mp4)
ffmpeg -i "$inpfile" -c:v libx265 "$flnBase".265.mp4
