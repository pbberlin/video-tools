ffmpeg -i input.mp4 -filter:v "setpts=0.96*PTS" -filter:a "atempo=1.0416667" -r 25 output_25fps.mp4
