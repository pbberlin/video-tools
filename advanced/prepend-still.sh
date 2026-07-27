#!/bin/bash

# --- Input / Output Variables ---
INPUT_VIDEO="ken-shabby-edit-c-subtitles.mkv"
INPUT_TITLE="ken-shabby-title.jpg"
OUTPUT_VIDEO="output.mkv"
INTRO_DURATION="1.8" # Duration in seconds

# Get main video width and height using ffprobe
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$INPUT_VIDEO")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$INPUT_VIDEO")

# Convert intro duration to milliseconds for audio delay
DELAY_MS=$(awk "BEGIN {print int(${INTRO_DURATION} * 1000)}")

ffmpeg -y \
    -loop 1 -t "$INTRO_DURATION" -i "$INPUT_TITLE" \
    -i "$INPUT_VIDEO" \
    -filter_complex "\
        [0:v]scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=decrease,pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p[intro]; \
        [intro][1:v]concat=n=2:v=1:a=0[v]; \
        [1:a]adelay=${DELAY_MS}:all=1[a]" \
    -map "[v]" \
    -map "[a]" \
    -c:v libx264 -level 6.2 -crf 18 -preset slow \
    -g 1 -bf 0 -keyint_min 1 \
    -fps_mode cfr -r 25 \
    -c:a aac -b:a 192k \
    "$OUTPUT_VIDEO"