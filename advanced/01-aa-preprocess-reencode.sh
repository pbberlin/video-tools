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

fn="$1"  
outf="${fn//\.mp4/-renc.mp4}"


if [[ -z "$fn" ]]; then
        echo "filename - first arg - missing "
        exit 1
else
        echo "converting fn '$fn' to 1 b-frame every 5 frames - '$outf' "
        echo "  "
fi 

ffmpeg -i "./$fn"   -c:v libx264  -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   $outf



