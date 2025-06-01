# does not help
# re-encode with davinci resolve

filename="$1"
ffmpeg -i "$filename" -fflags +genpts -c copy "$flnBase-fixedts.mp4"
