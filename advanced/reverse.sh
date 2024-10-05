# video only:
ffmpeg -i ./p08.mp4 -vf reverse p08-reversed.mp4


# audio and video:
ffmpeg -i /storage/emulated/0/ffvid/frameCount.mp4 -vf reverse -af areverse reversed.mp4
