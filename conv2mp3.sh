# "C:\Program Files\Git\git-bash.exe"
# conv2mp3.sh
echo "Encoding -$1-"

ffmpeg -i "./$1" -vn \
       -acodec libmp3lame -ac 2 -ab 160k -ar 48000 \
        "$1.mp3"

# specific directoy
# ffmpeg -i "/c/Users/pbu/Downloads/video/conv/$1" -vn \
#        -acodec libmp3lame -ac 2 -ab 160k -ar 48000 \
#         "$1.mp3"

# Variable bitrate; https://askubuntu.com/questions/84584/converting-mp4-to-mp3
# ffmpeg -i video.mp4 -vn \
#        -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 \
#         audio.mp3