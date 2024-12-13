# Step b
# create clips from a long video
# ============================

# clip - no re-encoding
#   fast - clips are glitchy if B-frames are sparse
#   fast - clips are good - if previously re-encoded
ffmpeg -i p01.mp4 -ss 00:00:00 -to 00:00:02 -c copy p01-1.mp4


# clip  -    re-encoding
#   this creates nice clips, that are easy to play with VLC
#   Takes some time - but is essential.
#   -c:v libx264 - much bigger but much faster
ffmpeg -i inp.mp4  -c:v libx264 -level 6.2 -crf 18   -ss 00:04.000     -to 00:00:08.000         out-04-08.mp4
ffmpeg -i inp.mp4  -c:v libx264 -level 6.2 -crf 18   -ss 00:17.000     -to 00:00:25.000         out-17-25.mp4
ffmpeg -i inp.mp4  -c:v libx264 -level 6.2 -crf 18   -ss 00:38.000     -to 00:00:47.000         out-18-47.mp4



# removing audio from  output (optional)
-an

# copy audio
-c:a copy



