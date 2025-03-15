#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "converting dir $dir to h.256"
        echo "  "
fi


# first  extension
for filename in "${dir}"/*.mp4 ; do
        flnBase=$(basename "$filename" .mp4)
        echo "re-coding -${flnBase}- to h.256"
        ffmpeg -i "$filename" -c:v libx265 -vtag hvc1 "$flnBase.256.mp4"
done

# second extension
for filename in "${dir}"/*.mkv ; do
        flnBase=$(basename "$filename" .mkv)
        echo "re-coding -${flnBase}- to h.256"
        ffmpeg -i "$filename" -c:v libx265 -vtag hvc1 "$flnBase.256.mp4"
done

