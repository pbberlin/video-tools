#!/bin/bash

inpDir=./resized

outDir=./zoomed
mkdir "${outDir}" -p

# -loop 1: loops the image indefinitely.
# -vf "zoompan=z='min(zoom+0.0015,1.5)':d=30*4"
#        (zoom+0.0015,1.5) - zoom out by a factor of 0.0015 each frame until the zoom level reaches 1.5.
#        d=30*4            - sets the duration of each frame to 120 frames (4 seconds at 30 fps).
#       -c:v mpeg2video    - video codec to MPEG-2
#       -t 5               - duration of the video to 5 seconds.
#       -r 30              - rate to 30 frames per second.

#   x='iw/2-(iw/zoom/2)': centers zoom horizontally  - iw is input width
#   y='ih/2-(ih/zoom/2)': Centers zoom vertically    - ih is input height


for img in ./${inpDir}/*.jpg; do

  flnBase=$(basename "$img" .jpg)
  outPath1="./${outDir}/${flnBase}-c.mp4"

  # # center
  # ffmpeg -loop 1 -i "$img" \
  #        -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=30*4,scale=w=3840:h=2880,setsar=1/1" \
  #        -c:v libx264 -s 3840x2880 -t 4.5 -r 30 "$outPath1"

  # # top left
  # outPath2="./${outDir}/${flnBase}-tl.mp4"
  # ffmpeg -loop 1 -i "$img" \
  #        -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/3-(iw/zoom/2)':y='ih/3-(ih/zoom/2)':d=30*4,scale=w=3840:h=2880,setsar=1/1" \
  #        -c:v libx264 -s 3840x2880 -t 4.5 -r 30 "$outPath2"

  # # center left
  # outPath3="./${outDir}/${flnBase}-cl.mp4"
  # ffmpeg -loop 1 -i "$img" \
  #        -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/3.5-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=30*4,scale=w=3840:h=2880,setsar=1/1" \
  #        -c:v libx264 -s 3840x2880 -t 4.5 -r 30 "$outPath3"

  # top center
  outPath3="./${outDir}/${flnBase}-tc.mp4"
  ffmpeg -loop 1 -i "$img" \
         -vf "zoompan=z='min(zoom+0.001,1.2)':x='iw/2-(iw/zoom/2)':y='ih/3.5-(ih/zoom/2)':d=30*4,scale=w=3840:h=2880,setsar=1/1" \
         -c:v libx264 -s 3840x2880 -t 4.5 -r 30 "$outPath3"


done
