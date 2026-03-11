#!/bin/bash

dir="$1"
deletePng="$2"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing - assuming '.' "
        dir="."
else
        echo "converting PNG files in dir $dir to JPG"
        echo "  "
fi


shopt -s nullglob

for fn in "${dir}"/*.png "${dir}"/*.PNG ; do
        baseName="${fn%.*}"
        outf="${baseName}.jpg"

        echo "   checking -${fn}- for alpha channel..."

        alphaStats=$(ffmpeg -v info -i "$fn" -vf "alphaextract,signalstats,metadata=print" -f null - 2>&1)
        alphaMin=$(echo "$alphaStats" | grep -o "lavfi.signalstats.YMIN=[0-9]*" | cut -d= -f2)
        alphaMax=$(echo "$alphaStats" | grep -o "lavfi.signalstats.YMAX=[0-9]*" | cut -d= -f2)

        if [[ -z "$alphaMin" || -z "$alphaMax" ]]; then
                echo "   WARNING: could not evaluate alpha — assuming real transparency"
                echo "   ${alphaStats}"
                hasRealAlpha=1

        elif [[ "$alphaMin" -ge 253 && "$alphaMax" -eq 255 ]]; then
                echo "     alpha fully opaque — including file"

        elif [[ "$alphaMin" -eq "$alphaMax" ]]; then
                echo "     alpha uniform ($alphaMin) — including file"

        else
                echo "     real mask detected (min=$alphaMin max=$alphaMax)"
                hasRealAlpha=1
        fi


        if [[ "$hasRealAlpha" -eq 1 ]]; then
                echo "   skipping $fn (contains real transparency)"
                continue
        fi


        echo "   converting -${fn}- to ${outf}..."

        # 2–5 = very good
        # 6–15 = medium
        # 20+ = low quality
        ffmpeg -i "$fn" -q:v 2 "$outf"

        if [[ $? -ne 0 ]]; then
                echo "   ERROR converting $fn"
                continue
        fi

        if [[ "$deletePng" == "--delete" ]]; then
                echo "   deleting original $fn"
                rm "$fn"
        fi

done