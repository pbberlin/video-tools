for filename in ./dir/*.mp4; do
        echo "Encoding -$filename-"
        ffmpeg -i "$filename" -vn \
        -acodec libmp3lame -ac 2 -ab 128k -ar 48000 \
                "$filename.mp3"
done