fn="$1"  
outf="${fn//\.mp4/-stabilized.mp4}"


if [[ -z "$fn" ]]; then
        echo "filename - first arg - missing "
        exit 1
else
        echo "stabilizing fn '$fn' to '$outf' "
        echo "  "
fi 

# shakiness=10: Analyzes stronger shakes (min 1, default 5, max 10).
# accuracy=15:  Increases precision (1-15).
# stepsize=6:   1-32
ffmpeg -i "./$fn" -vf vidstabdetect=result=transforms.trf:shakiness=10:accuracy=15:stepsize=32 -f null -

# zoom=5:        Prevents black borders by zooming slightly.
# optzoom=1:     Automatically optimizes zoom.
# smoothing=100: Reduce jitter (default 10, higher means smoother, over 100 may cause lag/delay).
ffmpeg -i "./$fn" -level 6.2 -crf 18  -preset slow  -vf vidstabtransform=input=transforms.trf:zoom=10:optzoom=1:smoothing=1000   -g  5  -bf 1  -b_strategy 0    $outf




