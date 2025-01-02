# Step a
# re-encode for easy editing
# ============================


# re-encode at high quality - force regular b-frames
# bframe settings
#
#    -level         https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding_tiers_and_levels
#   -g  10          GOP - group of pictures size
#   -bf  1          at least one bframe per GOP
#   -b_strategy 0   disable adaptive behavior

#
#   -crf  0         no compression ??
#   -crf 18         max quality - variable bitrate
#   -b:v 50M        max constant bitrate -
#                   50M is the maximum possible at level 4.1
#                   for streaming at constant rate

ffmpeg -i input.mp4 -c:v libx264 -c:v libx264  -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4





# H.265 to H.264 for DaVinci Resolve
#   Some video edit software does not work well with highly compressed H.265 mp4 files.
#   We want to re-encode to H.264 - clips get 2.5 times larger
ffmpeg -i input.mp4 -map 0 -c:v libx264 -crf 18 -preset slower -c:a copy output-h264-18.mkv

# 265 yields increased file size
ffmpeg -i input.mp4 -map 0 -c:v libx265 -crf 23 -preset slower -c:a copy output-h265-23.mkv

# this is smaller than 265:
ffmpeg -i input.mp4 -map 0 -c:v libx264 -crf 23 -preset slower -c:a copy output-h264-23.mkv











