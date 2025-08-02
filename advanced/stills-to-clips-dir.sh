#!/usr/bin/env bash
set -euo pipefail

fps=25
dur=2.5

# number of frames the zoompan filter should emit
frames="$(awk -v f="$fps" -v d="$dur" 'BEGIN{printf "%d", f*d}')"

for img in ./*.jpg; do

    flnBase="$(basename "${img%.*}")"

    outStill="${flnBase}-still.mkv"
    outCenter="${flnBase}-center.mkv"
    outTopLeft="${flnBase}-tl.mkv"

    echo ">>> ${img} -> ${outStill}"    
    ffmpeg -y -loop 1 -i "$img" \
           -c:v libx264 -t 2 -pix_fmt yuv420p -r 25 \
           -an "$outStill"

    echo ">>> ${img} -> ${outCenter}"
    ffmpeg -y -loop 1 -i "$img" \
        -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames},fps=${fps},setsar=1/1" \
        -c:v libx264 -t "$dur" -r "$fps" -an "$outCenter"

    echo ">>> ${img} -> ${outTopLeft}"
    ffmpeg -y -loop 1 -i "$img" \
        -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/3-(iw/zoom/2)':y='ih/3-(ih/zoom/2)':d=${frames},fps=${fps},setsar=1/1" \
        -c:v libx264 -t "$dur" -r "$fps" -an "$outTopLeft"
done
