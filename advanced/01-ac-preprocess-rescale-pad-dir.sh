#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "rescaling and padding $dir to 3840 x 2880"
        echo "  "
fi


# first  extension
# for filename in "${dir}"/*.mkv ; do
for filename in "${dir}"/*.mp4 ; do
        flnBase=$(basename "$filename" .mp4)
        echo "re-scaling -${flnBase}- to 3840 x 2880"
        # ffmpeg -i "$filename" -c:v libx264  -filter:v "scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   "$flnBase-rescaled.mp4"
        ffmpeg -i "$filename" -c:v libx264  -filter:v "scale='min(3840,iw*2880/ih)':'min(2880,ih*3840/iw)',pad=3840:2880:(3840-iw*2880/ih)/2:(2880-ih*3840/iw)/2:black" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   "$flnBase-rescaled.mp4"
done


