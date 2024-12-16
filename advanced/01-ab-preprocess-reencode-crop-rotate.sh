# re-encode and crop  
#
#  format: width:height:x:y
#
#  input   3840 x 2880  - 1,333
#  input   1920 x 1080  - 1.777
#
# -filter:v "crop=960:540:480:80"
ffmpeg -i input.mkv -c:v libx264  -filter:v "crop=960:540:480:80" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4


#
# scaling output:   ,scale=w=3840:h=2880
ffmpeg -i input.mp4 -c:v libx264  -filter:v "crop=3640:2680:100:100,scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4







# rotale freely


#    border 120px
#       3600:2640:120:120
ffmpeg -i input.mp4 -c:v libx264  -filter:v "rotate=+08.0*(PI/180):bilinear=0,crop=3600:2640:120:120,scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4

#    border 240px
#       3360:2400:240:240
ffmpeg -i input.mp4 -c:v libx264  -filter:v "rotate=+08.0*(PI/180):bilinear=0,crop=3360:2400:240:240,scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4

#    border 420px
#       3000:2040:420:420
ffmpeg -i input.mp4 -c:v libx264  -filter:v "rotate=-12.0*(PI/180):bilinear=0,crop=3000:2040:420:420,scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4

#    border 480px
#       3840-960=2880 
#       2880-960=1920 
#       2880:1920:480:480
ffmpeg -i input.mp4 -c:v libx264  -filter:v "rotate=-22.5*(PI/180):bilinear=0,crop=2880:1920:480:480,scale=w=3840:h=2880" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   output.mp4






# rotate 90° 
ffmpeg -i input.mp4 -c:v libx264  -filter:v "transpose=cclock,..."     
