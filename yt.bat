@REM https://github.com/yt-dlp/yt-dlp
@REM pip install --upgrade yt-dlp
@REM   --write-sub
@REM yt-dlp  -f "bestvideo[height<=480]+bestaudio/best[height<=480]"   --recode-video mp4  %1
yt-dlp  -f "bestvideo[height<=480]+bestaudio/best[height<=480]" --write-sub  --recode-video mp4  %1