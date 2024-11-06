# simple cromakey
ffmpeg -i input.mp4 -vf "chromakey=0x00FF00:0.3:0.1, hqdn3d=1.5:1.5:6:6" -c:v libx264 -c:a copy output.mp4

# export and re-assemble
ffmpeg -i input.mp4 -vf "fps=30" frames/output_%04d.png
# put through rem-bg...

# re-assemble
ffmpeg -framerate 30 -i frames/output_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
