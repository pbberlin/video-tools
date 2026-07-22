#!/bin/bash


# Step a
# re-encode for easy editing
# ============================


# re-encode at high quality - force regular b-frames
# bframe settings
#
#    -level         https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding_tiers_and_levels
#   -g  10          GOP - group of pictures size
#   -bf  1          at least one bframe per GOP
#   -b_strategy 0   disable adaptive behavior

#
#   -crf  0         no compression ??
#   -crf 18         max quality - variable bitrate
#   -b:v 50M        max constant bitrate -
#                   50M is the maximum possible at level 4.1
#                   for streaming at constant rate

dir="$1"
# dir="${1:-.}"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing - assuming '.' "
        dir="."
        # exit 1
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


