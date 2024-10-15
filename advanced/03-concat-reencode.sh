# stackoverflow.com/questions/7333232/
# simple concatenation - result suffers from itchy playpack
#   do not use
ffmpeg -f concat -i input-list.txt  -c copy concatenated.mp4



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

# duration    - duration of crossfade in seconds


#  crossfade 2 inputs
#     p01.mp4  is 2.5 seconds long
#     we start at 2.2 seconds - and make it 0.6 seconds long
ffmpeg -i p01.mp4 -i p02.mp4 ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v][1:v]xfade=transition=fade:duration=0.6:offset=2.2[outv]" ^
  -crf 18 ^
  -map "[outv]" -an crossf-tmp1.mp4




#  subsequent with result of previous output
#    crossf-tmp1.mp4 is 5.033 seconds long
ffmpeg -i crossf-tmp1.mp4 -i p03.mp4 ^
  -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v][1:v]xfade=transition=fade:duration=0.6:offset=4.7[outv]" ^
  -crf 18 ^
  -map "[outv]" -an crossf-tmp2.mp4




# example using start_frame instead of offset
ffmpeg -i p01.mp4 -i p02.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=1:start_frame=90[outv]" \
-map "[outv]" -an output.mp4


# the parameters get even more complex for longer chains of clips:

#  crossfade 3 inputs
ffmpeg -i p01.mp4 -i p02.mp4 -i p03.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v01]; \
[v01][2:v]xfade=transition=fade:duration=1:offset=8[outv]" \
-map "[outv]" -an re-enc-1-3-crossf.mp4



