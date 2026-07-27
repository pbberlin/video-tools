ffmpeg -i ken-shabby-edit-c.mkv \
    -vf "subtitles=ken-shabby-edit-c.srt" \
    -g 1  -bf 0  -keyint_min 1    \
    -vsync cfr   -r 25 \
    -c:a copy \
    ken-shabby-edit-c-subtitles.mkv