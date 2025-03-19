#!/bin/bash

pth="$1"

if [[ -z "$pth" ]]; then
        echo "work pth - first arg - missing "
        exit 1
else
        echo "converting pth $pth to 1 b-frame every 5 frames"
        echo "  "
fi


# first  extension
# for filename in "${pth}"/*.mkv ; do
for filename in "${pth}"; do
        flnBase=$(basename "$filename" .mp4)
        echo "re-coding -${flnBase}- to 1 b-frame every 5 frames"
        ffmpeg -i "$filename" -c:v libx264  -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   "$flnBase-renc.mp4"
done


