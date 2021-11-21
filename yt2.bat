@REM https://github.com/ytdl-org/youtube-dl
@REM   --write-sub
@REM youtube-dl  -f "bestvideo[height<=480]+bestaudio/best[height<=480]"   --recode-video mp4  %1
youtube-dl  -f "bestvideo[height<=2160]+bestaudio/best[height<=2160]" --write-sub  --recode-video mp4  %1