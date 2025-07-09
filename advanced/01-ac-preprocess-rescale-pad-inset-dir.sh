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
        outf1="${baseName}-pad-inset.mkv"
        outf2="${baseName}-pad-inset-rescaled.mkv"
        echo "    padding / insetting -${baseName}- ${outf1} to to top 85%"
        # -filter:v "scale='min(3840,iw*2880/ih)':'min(2880,ih*3840/iw)',pad=3840:2880:(3840-iw*2880/ih)/2:(2880-ih*3840/iw)/2:black"  \
 
        # first step - add padding - increasing width and height of output
        ffmpeg -i "$fn" -c:v libx264   \
                -level 6.2 -crf 18  -preset slow \
                -vf "pad=iw*1.15:ih*1.15:(ow-iw)/2:0:black" \
                "./${outDir}/$outf1"


        # second step - re-scale to original with and height
        #    steps cannot be comined
        prevWidth=$( ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$fn")
        prevHeight=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$fn")

        ffmpeg -i "./${outDir}/$outf1" -c:v libx264   \
                -level 6.2 -crf 18  -preset slow \
                -vf "scale=$prevWidth:$prevHeight" \
                "./${outDir}/$outf2"
done


