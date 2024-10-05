# stackoverflow.com/questions/7333232/
# simple concatenation - result suffers from itchy playpack
ffmpeg -f concat -i input-list.txt  -c copy concatenated.mp4



# concat and re-encode
# https://trac.ffmpeg.org/wiki/Concatenate

# with audio
# ffmpeg -i p1.mp4 -i p2.mp4 -i p3.mp4 \
# -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" \
# -map "[v]" -map "[a]" re-enc.mp4



# two
ffmpeg -i p07-slow-segment-1.mp4 -i p07-slow-segment-2.mp4   ^
  -filter_complex ^
  "[0:v:0][1:v:0]concat=n=2:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  concat-reenc-2parts.mp4


# 1-2-2a-3
ffmpeg -i p01.mp4 -i p02.mp4 -i p02a.mp4 -i p03.mp4  ^ 
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0]concat=n=4:v=1[outv]" ^
  -map "[outv]"  re-enc-1-3a.mp4


# 7 pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p02a.mp4 -i p03.mp4 -i p04.mp4 -i p05.mp4 -i p06.mp4   ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0][4:v:0][5:v:0][6:v:0]concat=n=7:v=1[outv]" ^
  -map "[outv]"  re-enc-1-7.mp4



# 9 pieces
ffmpeg -i p01.mp4 -i p02.mp4 -i p02a.mp4 -i p03.mp4 -i p06.mp4 -i p07.mp4  -i p08.mp4  -i p09.mp4  -i p11.mp4    ^
   -c:v libx264 -level 4.1 ^
  -filter_complex ^
  "[0:v:0][1:v:0][2:v:0][3:v:0][4:v:0][5:v:0][6:v:0][7:v:0][8:v:0]concat=n=9:v=1[outv]" ^
  -crf 18 ^
  -map "[outv]"  re-enc-1-9.mp4


####

#  crossfade 2 inputs
ffmpeg -i p1.mp4 -i p2.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=0.2:offset=1.468[outv]" \
-map "[outv]" -an re-enc-1-2-crossf.mp4


#  crossfade 2 inputs
ffmpeg -i re-enc-1-2-crossf.mp4 -i p3.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=0.2:offset=2.269[outv]" \
-map "[outv]" -an re-enc-1-2-3-crossf.mp4


#  crossfade 3 inputs
ffmpeg -i p1.mp4 -i p2.mp4 -i p3.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v01]; \
[v01][2:v]xfade=transition=fade:duration=1:offset=8[outv]" \
-map "[outv]" -an re-enc-1-3-crossf.mp4



