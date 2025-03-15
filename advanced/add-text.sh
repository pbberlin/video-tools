


# -c:a copy - Copies the audio without re-encoding



#  seems, we dont need the colon in C:
ffmpeg -i with-audio.mp4   \
  -vf "drawtext=text='Neindorf - road to Beckendorf':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,1.2,8.2)',  \
     drawtext=text='August 2024':fontfile=C\\\\Windows\\\\Fonts\\\\GOTHIC.TTF:fontcolor=white:fontsize=256:x=(w-text_w)/2:y=(h-text_h)-128:bordercolor=white:borderw=2:enable='between(t,8.7,10.2)'  \
  " \
  -c:a copy \
  -c:v libx264 \
  output-with-subs.mp4


# ttf file in same dir

ffmpeg -i input.mp4   \
  -vf " drawtext=text='1':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,0.1,1.9)'   , \
        drawtext=text='2':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,2.1,5.9)'   , \
        drawtext=text='3':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,6.1,7.9)'   , \
        drawtext=text='4':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,8.1,9.9)'   , \
        drawtext=text='5':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,10.1,11.9)' , \
        drawtext=text='6':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,12.1,13.9)' , \
        drawtext=text='7':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,14.1,15.9)' , \
        drawtext=text='8':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,16.1,17.9)' , \
        drawtext=text='9':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,18.1,19.9)' , \
       drawtext=text='10':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,20.1,21.9)' , \
       drawtext=text='11':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,22.1,23.9)' , \
       drawtext=text='12':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,24.1,25.9)' , \
       drawtext=text='13':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,26.1,27.9)' , \
       drawtext=text='14':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,28.1,29.9)' , \
       drawtext=text='15':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,30.1,32.9)' , \
       drawtext=text='16':fontfile=GothicA1-Regular.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/1-20:y=(h-text_h)-12:bordercolor=white:borderw=2:enable='between(t,33.1,35.9)' , \
  " \
  -c:a copy \
  -c:v libx264 \
  -level 5.1 -crf 18 \
  -g 10  -bf 4 \
  output-numbered.mp4





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
