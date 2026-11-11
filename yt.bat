@REM  uv pip install --system -U yt-dlp 
@REM   https://github.com/yt-dlp/yt-dlp
python -m yt_dlp -f  "bestvideo[height<=480]+bestaudio/best[height<=480]" --write-sub  --recode-video mp4  %1