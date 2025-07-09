#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "converting dir $dir to every frame is a key frame - frame rate 25"
        echo "  "
fi


# for fn in "${dir}"/*.mp4 ; do
for fn in "${dir}"/*.mkv ; do
        baseName="${fn%.*}"
        outf="${baseName}-reenc.mkv"

        echo "   re-encoding -${fn}- to ${outf}..."
        ffmpeg -i "$fn"    -c:v libx264  -level 6.2 -crf 18  -preset slow   \
        -g 1  -bf 0  -keyint_min 1    \
        -vsync cfr   -r 25 \
        "$outf"

done


