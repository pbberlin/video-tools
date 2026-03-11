#!/bin/bash

set -euo pipefail

shopt -s nullglob
shopt -s nocaseglob           # match .MP4 as well as .mp4

# work dir - or default ".s"
dir="${1:-.}"


echo "creating movie thumbs for dir $dir"
echo "  "

# temp workspace
tmpRoot="$(mktemp -d)"
cleanup() { rm -rf "$tmpRoot"; }
trap cleanup EXIT


# four timestamps: 0s,10s,20s,30s
tsList=(0 10 20 30)

for fn in "$dir"/*.{mkv,mp4}; do
  
  # skip if the glob didn't match anything
  [[ -e "$fn" ]] || continue

  baseName="${fn%.*}"
  outPng="${baseName}-thumb.png"
  outWbp="${baseName}-thumb.webp"

  echo "processing: $fn"
  workDir="$(mktemp -d "$tmpRoot/frames.XXXX")"

  # 1) Extract frames (seek before -i for faster, accurate cuts)
  idx=0
  for t in "${tsList[@]}"; do
    printf -v num "%02d" "$idx"
    ffmpeg -y -ss "$t" -i "$fn" -frames:v 1 -vf "scale=320:-2" \
      "$workDir/frame_${num}.png" < /dev/null
    idx=$((idx+1))
  done


  # 2) 2x2 grid from 4 frames
  ffmpeg -y -framerate 1 -i "$workDir/frame_%02d.png" \
    -vf "tile=2x2:padding=10:margin=10,format=rgb24" \
    -frames:v 1 "$outPng" < /dev/null


  # 3) Animated WebP (1 fps, loop forever)
  ffmpeg -y -framerate 1 -i "$workDir/frame_%02d.png" \
    -vf "format=rgba" -loop 0 -c:v libwebp -q:v 70 -compression_level 6 \
    "$outWbp" < /dev/null


  echo "wrote: $outPng"
  echo "wrote: $outWbp"
done



