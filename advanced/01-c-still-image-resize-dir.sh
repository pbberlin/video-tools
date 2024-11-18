#!/bin/bash

# resize JPG images in directory from 4080x3072  to 3840x2880  


#  -q:v 2
#      2:   High quality
#      5:   Good quality
#     10: Medium quality.

inpDir=./raw

outDir=./resized
mkdir "${outDir}" -p

for img in ./${inpDir}/*.jpg; do
  flnBase=$(basename "$img" .jpg)
  outPath="./${outDir}/${flnBase}.jpg"
  ffmpeg -i "$img" -vf "scale=3840:2880"  -q:v 2 "$outPath"
done
