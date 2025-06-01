#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "converting dir $dir to mkv"
        echo "  "
fi


for fn in "${dir}"/*.mp4 ; do
        baseName="${fn%.*}"
        outf="${baseName}.mkv"
        echo "   conv -${fn}- to ${outf}..."
        ffmpeg -i "$fn" -c copy "$outf"
done


