#!/bin/bash


#  no encoding

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "fixing timestamps for $dir"
        echo "  "
fi


for filename in "${dir}"/*.mp4 ; do
        flnBase=$(basename "$filename" .mp4)
        echo "fixing timestamps -${flnBase}- "
        ffmpeg -i "$filename" -fflags +genpts -c copy "$flnBase-fixedts.mp4"

done

