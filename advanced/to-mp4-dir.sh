#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing - assuming '.' "
        dir="."
        # exit 1
else
        echo "converting dir $dir back to mpg"
        echo "  "
fi


for fn in "${dir}"/*.mkv ; do
        baseName="${fn%.*}"
        outf="${baseName}.mp4"
        echo "   conv -${fn}- to ${outf}..."
        ffmpeg -i "$fn" -c copy "$outf"
done


