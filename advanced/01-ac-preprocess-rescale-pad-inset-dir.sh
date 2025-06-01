#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "rescaling and padding $dir to top 85%"
        echo "  "
fi

outDir=./pad-inset
mkdir "${outDir}" -p

# first  extension
for fn in "${dir}"/*.mkv ; do
        baseName="${fn%.*}"
        outf="${baseName}-pad-inset.mkv"
        echo "    padding / insetting -${baseName}- ${outf} to to top 85%"
        # -filter:v "scale='min(3840,iw*2880/ih)':'min(2880,ih*3840/iw)',pad=3840:2880:(3840-iw*2880/ih)/2:(2880-ih*3840/iw)/2:black"  \
        # -filter:v "scale='min(1680,iw*1120/ih)':'min(1120,ih*1680/iw)',pad=1680:1120:(1680-iw*1120/ih)/2:(1120-ih*1680/iw)/2:black"  \
        # much better
        # -vf "pad=iw:ih*1.15:(ow-iw)/2:0" \
        ffmpeg -i "$fn" -c:v libx264   \
                -level 6.2 -crf 18  -preset slow \
                -vf "pad=iw:ih*1.15:(ow-iw)/2:0" \
                "./${outDir}/$outf"
done


