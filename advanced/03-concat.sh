# stackoverflow.com/questions/7333232/
# simple concatenation - result suffers from itchy playpack
#   only use with clips that have been preprocessed with dense b-frames
dir /b > input-list.txt 
# prepend "file " to the lines

# 03a-concat-fix-timestamps-dir.sh - does not help
ffmpeg -f concat   -i input-list.txt  -c copy concatenated.mp4






# concat and re-encode
# https://trac.ffmpeg.org/wiki/Concatenate


# some command lines to combine a number of clips - 
#   re-encoding them for regular b-frames

# the syntax gets ever more convoluted, with rising number of clips.
#   since the quality loss is neglible, we can combine ever larger chunks


# four pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -i p04.mp4  ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0]concat=n=4:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  re-enc-1-4.mp4


# seven pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -i p04.mp4 -i p05.mp4 -i p06.mp4 -i p07.mp4   ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0][4:v:0][5:v:0][6:v:0]concat=n=7:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  re-enc-1-7.mp4



# nine pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -i p04.mp4 -i p05.mp4 -i p06.mp4  -i p07.mp4  -i p08.mp4  -i p09.mp4    ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0][4:v:0][5:v:0][6:v:0][7:v:0][8:v:0]concat=n=9:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  re-enc-1-9.mp4


# 13 pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -i p04.mp4 -i p05.mp4 -i p06.mp4  -i p07.mp4  -i p08.mp4  -i p09.mp4   -i p10.mp4 -i p11.mp4 -i p12.mp4 -i p13.mp4    ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0][4:v:0][5:v:0][6:v:0][7:v:0][8:v:0][9:v:0][10:v:0][11:v:0][12:v:0]concat=n=13:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  re-enc-1-13.mp4







# three pieces - with audio
#    this makes the syntax even more convoluted
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 ^
  -c:v libx264 -level 4.1 ^
  -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [outv] [a]" ^
  -crf 18 ^
  -map "[outv]" -map "[a]" re-enc.mp4




####
# crossfade

# start_frame - frame where fading starts - relative to the segment
#    or
# offset      - time  where fading starts - relative to the segment

# duration    - HALF of duration of crossfade in seconds
#   time until the first clip ENDS


# example: crossfade 2 inputs
# where p01.mp4  is 2.5 seconds long
#
#       xfade=offset=2.2:duration=0.3
#             making output 0.3 seconds shorter than sum of inputs
#         or
#       xfade=offset=2.0:duration=0.5
#             making output 0.5 seconds shorter than sum of inputs
#         or
#       xfade=offset=1.5:duration=1.0
#             making output 1.0 seconds shorter than sum of inputs


# crossf-tmp1.mp4 is 0.3 seconds shorter
ffmpeg -i p01.mp4 -i p02.mp4 ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v][1:v]xfade=offset=2.2:duration=0.3[outv]" ^
  -crf 18 ^
  -map "[outv]" -an crossf-tmp1.mp4


#  continue to add clips to previous output:

#    measure exact length of privious output:
ffprobe -i crossf-tmp1.mp4
#     Duration 00:00:04.73
#  4.73 seconds minus 0.3 = 4.43

# more terse
ffprobe -i input.mp4  -show_entries format=duration -v quiet -of csv="p=0"



ffmpeg -i crossf-tmp1.mp4 -i p03.mp4 ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v][1:v]xfade=offset=4.43:duration=0.3[outv]" ^
  -crf 18 ^
  -map "[outv]" -an crossf-tmp2.mp4




# ----------------------------------------------

# we could try to combine three inputs with two crossfades...
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -filter_complex    \
"[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v01]; \
[v01][2:v]xfade=transition=fade:duration=1:offset=8[outv]" \
-map "[outv]" -an re-enc-1-3-crossf.mp4



