# Step 1
# create clips from a long video
# ============================

# cut out - no re-encoding
#   this is fast - but the clips are glitchy - because the B-frames are sparse
ffmpeg -i p01.mp4 -ss 00:00:00 -to 00:00:02 -c copy p01-1.mp4

# re-encode at high quality - force regular b-frames
# bframe settings
#   -g  10          GOP - group of pictures size
#   -bg  1          at least one bframe per GOP
#   -b_strategy 0   disable adaptive behavior

#
#   -crf 18         max quality - variable bitrate
#   -b:v 50M        max constant bitrate -
#                   50M is the maximum possible at level 4.1
#                   for streaming at constant rate
ffmpeg -i input.mp4 -c:v libx264 -level 5.1 -crf 18  -preset slow -g 10  -bf 4  -b_strategy 0   output.mp4


# cut out -    re-encoding
#   this creates nice clips, that are easy to play with VLC
#   Takes some time - but is essential.
#   -c:v libx264 - much bigger but much faster
ffmpeg -i inp.mp4  -c:v libx264 -level 5.1 -crf 18   -ss 00:04.000     -to 00:00:08.000         out-04-08.mp4
ffmpeg -i inp.mp4  -c:v libx264 -level 5.1 -crf 18   -ss 00:17.000     -to 00:00:25.000         out-17-25.mp4
ffmpeg -i inp.mp4  -c:v libx264 -level 5.1 -crf 18   -ss 00:38.000     -to 00:00:47.000         out-18-47.mp4




# removing audio from  output (optional)
-an

# We can also re-encode a clip - so it has proper b-frames
#     - -crf  0 -           no compression
#     - -crf 18 - virtually no compression
ffmpeg -i p07.mp4 -c:v libx264 -crf 18 -preset slow -c:a copy p07-re-encoded.mp4
ffmpeg -i p08.mp4 -c:v libx264 -crf 18 -preset slow -c:a copy p08-re-encoded.mp4


# H.265 to H.264 for DaVinci Resolve
#   Some video edit software does not work well with highly compressed H.265 mp4 files.
#   We want to re-encode to H.264 - clips get 2.5 times larger
ffmpeg -i p01.mp4 -map 0 -c:v libx264 -crf 18 -vf format=yuv420p -c:a copy p01-8bit.mkv








