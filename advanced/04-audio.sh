

#  replace audio
ffmpeg -i no-audio.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest with-audio.mp4


#  blend audio
ffmpeg -i no-audio.mp4 -i audio.mp3 -filter_complex "[0:a][1:a]amix=inputs=2:duration=shortest[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -shortest output.mp4


#  blend audio - set volume
#       original audio - reduce  to  50%
#       new      audio - amplify to 150% 
ffmpeg -i no-audio.mp4 -i audio.mp3 -filter_complex "[0:a]volume=0.5[a0];[1:a]volume=1.5[a1];[a0][a1]amix=inputs=2:duration=shortest[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -shortest output.mp4


