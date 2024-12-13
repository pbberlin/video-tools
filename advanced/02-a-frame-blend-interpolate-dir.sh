#!/bin/bash

dir="$1"

if [[ -z "$dir" ]]; then
        echo "work dir - first arg - missing "
        exit 1
else
        echo "converting dir $dir - interpolating 8 frames"
        echo "  "
fi

# loop 1 - create additional interpolated frames
for filename in "${dir}"/*.mp4 ; do
    flnBase=$(basename "$filename" .mp4)
    echo " -${flnBase}- "
    ffmpeg -i "$filename" -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" "$flnBase-240fps-sp256.mp4"
done

# loop 2 - slow output - results from previous loop
for filename in "${dir}"/*-240fps-sp256.mp4 ; do
    flnBase=$(basename "$filename" .mp4)
    echo " -${flnBase}- "
    ffmpeg -i "$filename" -vf "setpts=8*PTS" -r 30  "$flnBase-slow.mp4" 
done





