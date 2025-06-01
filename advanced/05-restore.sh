# -crf 23:        balance between quality and compression. range 20–24 
# -preset medium: reasonable compression. 
# -g 250:         standard GOP length (~10 seconds at 25 fps) for most streaming and storage purposes.
# -bf 3:          3 B-frames
# -b_strategy 1:  re-enables B-frame decision optimization


scale="384:-1" 
descr="tiny"

scale="768:-1" 
descr="medium"

scale="1280:-1"
descr="large"



fn="$1"  
baseName="${fn%.*}"
outf="${baseName}-${descr}.mkv"



ffmpeg -i "./$fn" \
  -c:v libx264 \
  -crf 23  \
  -preset medium \
  -g  250  \
  -bf   3  \
  -b_strategy 1 \
  -vf "scale=$scale"  \
  "$outf"