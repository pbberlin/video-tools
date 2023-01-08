# "C:\Program Files\Git\git-bash.exe"
# ./conv2h256-dir.sh
for filename in ./*.mkv; do
        echo "Re-coding -$filename- to h.256"
        ffmpeg -i "$filename" -c:v libx265 -vtag hvc1 "$filename.mp4"
done