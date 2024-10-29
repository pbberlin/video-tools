


# -c:a copy - Copies the audio without re-encoding



#  seems, we dont need the colon in C:
ffmpeg -i with-audio.mp4   \
  -vf "drawtext=text='Neindorf - road to Beckendorf':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,1.2,8.2)',  \
     drawtext=text='August 2024':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,8.7,10.2)'  \
  " \
  -c:a copy \
  -c:v libx264 \
  output.mp4



