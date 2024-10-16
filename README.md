# Video tools

## Youtube downloader

* Download any youtube video in various resolutions

* Dont use the browser URL,  
instead right-click on the video `copy video URL`

* Using [youtube-dl](https://en.wikipedia.org/wiki/Youtube-dl)  
hosted on [github.com](https://github.com/yt-dlp/yt-dlp)

```bash
pip install yt-dlp    --upgrade
```

* Put the the scripts `yt.bat`, `yt1.bat`, `yt2.bat` into your `c:\windows` directory.  
(you need admin rights to do this)

* Now you can open a command window in any directory and type  

```bash
yt [copied URL]
```

to download the youtube video.

* `yt1.bat` downloads the video in 1080 quality (larger file size)

* `yt2.bat` downloads the video in 2160 quality (huge file size)

## Audio extraction

* Install [ffmpeg](https://ffmpeg.org/download.html)

* Use `conv2mp3.sh` and `conv2mp3-dir.sh`  
to rip the audio from a downloaded youtube video.  
The second script converts _multiple_ videos from the directory `dir` at once.

## Web browser video streaming

* Use `streaming\conv.bat` to convert any video file  
into a streamable set of partitioned video files

* `index.m3u8` is the main file of the streamable video

* Use player1.html or player2.html to play a streamable video via web browser

* For this to work, `index.m3u8`... files have to reside on a http(s) server  
and have to emit an `allow cross domain` access header

## Convert to H.256

Re-encode existing `MPEG` files to `H.256` compression.

Saves about two thirds of files.

See `conv2h256-dir.sh`

## Scaling

```bash
ffmpeg -i input.mp4 -vf  scale=640:480 output.mp4
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4
```

## Rotate a video

<https://stackoverflow.com/questions/3937387/rotating-videos-with-ffmpeg>

```bash

# recode
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# recode, maintaining aspect ratio
#  https://stackoverflow.com/questions/8218363/maintaining-aspect-ratio-with-ffmpeg
ffmpeg -i input.mp4 -vf "transpose=2, scale=640:-2"   output-keep-2.mp4
ffmpeg -i input.mp4 -vf "transpose=2, scale=1080:-1"  output-keep-3.mp4


# only change metadata
ffmpeg -display_rotation 270 -i input.mp4 -codec copy output.mp4
```

## Advanced

A few ffmpeg command lines

The `^` is the line continuation char of windows cmd.  
No spaces after the `^`

For linux bash replace it with `\`.

* `01-a-create-clips-cutouts.sh`  
   * rough cut from raw video
   * select good clips

* `01-b-still-image-resize-dir.sh`, `01-b-still-image-zoom-dir.sh`
   * take any still image - from a photo or
      from a video - and expand it into a clip
   * all still images need to be resized to the destination video with and height
   * then the still can be made into small video clip with "camera pan"

* `02-cutouts--frame-blend-interpolate.sh`
   * some clips are very short - we want to lenghten them to fit the flow of the other clips
   * we compute intermediate frames and generate a longer clip

* `03-concat-reencode.sh`  
   * combine cuts with re-encoding - inserting stabilizing B-Frames
   * crossfading (experimental)

* `04-audio.sh`  
   * replace or add audio

* `reverse.sh` - make the clip play backward

