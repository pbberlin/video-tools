#!/bin/bash


# resizing image to fit target dimensions (3840x2880) 
# while preserving aspect ratio. 
# calculating optimal size for smaller dimension.
#     scale='min(3840,iw*2880/ih)':'min(2880,ih*3840/iw)'


# padding to center  within  target resolution.
#     pad=3840:2880:(3840-iw*2880/ih)/2:(2880-ih*3840/iw)/2:black: 

#  -q:v 2
#      2:   High quality
#      5:   Good quality
#     10: Medium quality.

inpDir=.
outDir=./resized-padded
mkdir "${outDir}" -p

for img in ./${inpDir}/*.jpg; do
  flnBase=$(basename "$img" .jpg)
  outPath="./${outDir}/${flnBase}.jpg"
  ffmpeg -i "$img" -vf "scale='min(3840,iw*2880/ih)':'min(2880,ih*3840/iw)',pad=3840:2880:(3840-iw*2880/ih)/2:(2880-ih*3840/iw)/2:black" -q:v 2 "$outPath"
done
