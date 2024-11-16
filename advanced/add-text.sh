


# -c:a copy - Copies the audio without re-encoding



#  seems, we dont need the colon in C:
ffmpeg -i with-audio.mp4   \
  -vf "drawtext=text='Neindorf - road to Beckendorf':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,1.2,8.2)',  \
     drawtext=text='August 2024':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,8.7,10.2)'  \
  " \
  -c:a copy \
  -c:v libx264 \
  output-with-subs.mp4



ffmpeg -i wolve.mp4   \
  -vf "drawtext=text='1':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,0.0,1.92)'  , \
       drawtext=text='2':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,3.0,4.5)'   , \
       drawtext=text='3':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,4.7,6.4)'   , \
       drawtext=text='4':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,6.55,7.8)'  , \
       drawtext=text='5':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,8.0,9.4)'   , \
       drawtext=text='6':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,9.55,11.4)' , \
       drawtext=text='7':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,11.5,12.8)' , \
       drawtext=text='8':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,12.9,14.9)' , \
       drawtext=text='9':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=32:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,15.0,17.5)' , \
  " \
  -c:a copy \
  -c:v libx264 \
  output-with-subs.mp4




# The kyrillic chars did not render

export LANG="en_US.UTF-8"

#  seems, we dont need the colon in C:
#    I copied the TTF files into the working dir
ffmpeg -i with-audio.mp4   \
  -vf "   \
      drawtext=text='Из тайги...'           :fontfile=DejaVuSans.ttf:fontcolor=black:fontsize=96:x=(w-text_w)/2:y=(h-text_h)-48:bordercolor=black:borderw=2:enable='between(t,0.2,2.0)',  \
      drawtext=text='...приходит Сашка...'  :fontfile=DejaVuSans.ttf:fontcolor=black:fontsize=96:x=(w-text_w)/2:y=(h-text_h)-48:bordercolor=black:borderw=2:enable='between(t,3.5,5.0)',  \
      drawtext=text='...я боюсь...'         :fontfile=DejaVuSans.ttf:fontcolor=black:fontsize=96:x=(w-text_w)/2:y=(h-text_h)-48:bordercolor=black:borderw=2:enable='between(t,5.0,6.5)'  \
  " \
  -c:a copy \
  -c:v libx264 \
  output-with-subs-3.mp4
