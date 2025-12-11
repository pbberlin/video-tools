# MPV installation


* https://mpv.io/
    * Install to C:\Program Files\mpv\


* https://github.com/stax76/mpv-hero
    * overwrite contents to mpv dir above
    * everything now in `portable_config`
            * app dir - script-*     can be removed
            * app dir - input.conf   can be removed
            * app dir - *.bat files  can be removed

    * Run C:\Program Files\mpv\installer\mpv-install.bat


* add to C:\Program Files\mpv\portable_config\scripts\
    encode.lua
    crop.lua

## save screenshot
s


## encode cropped area (press once to mark START, press ENTER to mark END)
e     script-message-to encode set-timestamp
ENTER script-message-to encode set-timestamp


## crop (occivink)
c     script-message-to crop start-crop

