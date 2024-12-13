# 
# rescale to stay within limits for macro block rate (MB rate)
# avoid errors such as
#      MB rate (xxxx) > level limit (983040)
-vf "scale=iw*0.5:ih*0.5"
-vf "scale=-1:1080"   
-vf "scale=1920:1080"   


ffmpeg -loop 1 -t 2.0 -i img1.jpg \
       -vf "scale=-1:1080"  \
       -r 30 -c:v libx264 -level 6.2 -pix_fmt yuv420p  -crf 18  -g 10  -bf 4  -b_strategy 0   -t 4 img1.mp4

ffmpeg -loop 1 -t 3.0 -i img2.jpg \
       -vf "scale=-1:1080"  \
       -r 30 -c:v libx264 -level 6.2 -pix_fmt yuv420p  -crf 18  -g 10  -bf 4  -b_strategy 0   -t 4 img2.mp4



# -t duration (input/output)
#      if used before -i - as input option: limit the duration of data read from the input file.

# slideshow video with one image per second
ffmpeg -framerate 1 -pattern_type glob -i '*.jpg' \
       -vf "scale=-1:1800"  \
       -r 30  -c:v libx264 -level 6.2 -pix_fmt yuv420p -crf 18  -g 10  -bf 4  -b_strategy 0   out2.mp4


# each image shown four seconds 
ffmpeg -framerate 0.25 -pattern_type glob -i '*.jpg' \
       -r 30  -c:v libx264 -level 6.2 -pix_fmt yuv420p -crf 18  -g 10  -bf 4  -b_strategy 0   out4.mp4


#  now the cross fade

#  -crf 18 seems better for replay than -b:v 50M 
ffmpeg -i img1.mp4 -i img2a.mp4 \
  -c:v libx264 -level 6.2  -crf 18  -preset slow  \
  -filter_complex "[0:v][1:v]xfade=offset=1.0:duration=1.0[outv]" \
  -g  5  -bf 4  -b_strategy 0   \
  -map "[outv]" -an tmp.mp4

ffmpeg -i tmp.mp4 -i img2b.mp4 \
  -c:v libx264 -level 6.2  -crf 18  -preset slow  \
  -filter_complex "[0:v][1:v]xfade=offset=3.0:duration=1.0[outv]" \
  -g  5  -bf 4  -b_strategy 0   \
  -map "[outv]" -an output.mp4




