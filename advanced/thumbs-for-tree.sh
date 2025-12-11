#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
shopt -s nocaseglob
shopt -s globstar             # enable recursive ** expansion

rootDir="${1:-.}"
outDir="${2:-$rootDir/.thumbs}"

rootDir="${rootDir%/}"

echo "root dir   : $rootDir"
echo "output dir : $outDir"
echo

mkdir -p "$outDir"

tmpRoot="$(mktemp -d)"
cleanup() { rm -rf "$tmpRoot"; }
trap cleanup EXIT

tsList=(0 10 20 30)

processOne() {
  local src="$1"
  echo "processing: $src"

  local relPath="${src#$rootDir/}"
  local relNoExt="${relPath%.*}"
  local safeName="${relNoExt//\//--}"

  local outPng="$outDir/${safeName}-thumb.png"
  local outWebp="$outDir/${safeName}-thumb.webp"

  local workDir
  workDir="$(mktemp -d "$tmpRoot/frames.XXXX")"

  local idx=0
  for t in "${tsList[@]}"; do
    printf -v num "%02d" "$idx"
    ffmpeg -y -ss "$t" -i "$src" -frames:v 1 -vf "scale=320:-2" \
      "$workDir/frame_${num}.png" < /dev/null
    idx=$((idx+1))
  done

  ffmpeg -y -framerate 1 -i "$workDir/frame_%02d.png" \
    -vf "tile=2x2:padding=10:margin=10,format=rgb24" \
    -frames:v 1 "$outPng" < /dev/null

  ffmpeg -y -framerate 1 -i "$workDir/frame_%02d.png" \
    -vf "format=rgba" -loop 0 -c:v libwebp -q:v 70 -compression_level 6 \
    "$outWebp" < /dev/null

  echo "wrote: $outPng"
  echo "wrote: $outWebp"
  echo
}

for fn in "$rootDir"/**/*.{mkv,mp4}; do
  if [[ -e "$fn" ]]; then
    processOne "$fn"
  fi
done
