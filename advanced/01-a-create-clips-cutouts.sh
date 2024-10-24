# Step 1
# create clips from a long video
# ============================

# cut out - no re-encoding
#   this is fast - but the clips are glitchy - because the B-frames are sparse
ffmpeg -i p01.mp4 -ss 00:00:00 -to 00:00:02 -c copy p01-1.mp4


# cut out -    re-encoding
#   this creates nice clips, that are easy to play with VLC  
#   Takes some time - but is essential.
ffmpeg -i p01.mp4 -ss 00:00:00     -to 00:00:02.500         p01-segment.mp4
ffmpeg -i p02.mp4 -ss 00:00:00.300 -to 00:00:02.825         p02-segment.mp4
ffmpeg -i p03.mp4 -ss 00:00:00     -to 00:00:02.500         p03-segment.mp4
ffmpeg -i p05.mp4 -ss 00:00:00     -to 00:00:06.500         p05-segment.mp4
ffmpeg -i p06.mp4 -ss 00:00:00     -to 00:00:01.400         p06-segment.mp4
ffmpeg -i p07.mp4 -ss 00:00:00.267 -to 00:00:03.871         p07-segment.mp4
ffmpeg -i p08.mp4 -ss 00:00:01.605 -to 00:00:05.711         p08-segment.mp4
ffmpeg -i p09.mp4 -ss 00:00:00.500 -to 00:00:05.906         p09-segment.mp4
ffmpeg -i p11.mp4 -ss 00:00:00.500                          p11-segment.mp4


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








