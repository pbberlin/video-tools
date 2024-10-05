# insert interpolated frames
# ============================

# http://underpop.online.fr/f/ffmpeg/help/minterpolate.htm.gz

# mi_mode - motion interpolation mode
# mi_mode=mci:   Motion-compensated interpolation mode.
# mi_mode=blend: blends two frames - instead of estimating motion vectors  

# mc_mode - motion compensation mode - default obmc
# mc_mode=aobmc: Advanced overlap block motion compensation - for motion estimation.
# mc_mode=obmc:  Overlap Block Motion Compensation can simplify the motion compensation model and reduce artifacts compared to aobmc

# me_mode - motion estimation mode - default is 'bilat'
# me_mode=bidir:


# me - motion estimation - default is 'epzs'
# :me=epzs      
# :me=ds
# :me=tss
# :me=esa

# mb_size - macroblock size - default 16
# :mb_size=64

# :search_param=32
# :search_param=64
# :search_param=128

# :vsbmc=1       variable-size block motion compensation; improve quality.
# :fps=60        desired output frame rate (i.e. 60 FPS)


ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'"                  p1-120fps.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240'"                  p1-240fps.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:search_param=128'" p1-120fps-sp128.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=128'" p1-240fps-sp128.mp4

ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" p1-240fps-sp256.mp4

ffmpeg -i p03.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" p03-240fps-sp256.mp4
ffmpeg -i p07.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" p07-240fps-sp256.mp4


# does not help very much
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=ds'"            p1-120fps-meds.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=tss'"           p1-120fps-metss.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=tss'"           p1-120fps-metss.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=esa'"           p1-120fps-meesa.mp4
ffmpeg -i p1.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=umh'"           p1-120fps-meumh.mp4







# slo-mo - footage with high FPS to framerate to 30
# ============================

# -vf "setpts=4*PTS": slow down the video by a factor of 4. 
#                     setpts filter adjusts the Presentation Timestamp (PTS),
#                     which controls the timing of frames.
# 4*PTS:              Multiplies PTS by 4, effectively making video 4 times slower.
# -r 30:              setting output frame rate to 30 FPS.
ffmpeg -i p1-120fps.mp4       -vf "setpts=4*PTS" -r 30 p1-120fps-slow.mp4
ffmpeg -i p1-120fps-sp128.mp4 -vf "setpts=4*PTS" -r 30 p1-120fps-sp128-slow.mp4

ffmpeg -i p5-240fps.mp4       -vf "setpts=8*PTS" -r 30 p5-240fps-slow.mp4
ffmpeg -i p1-240fps-sp128.mp4 -vf "setpts=8*PTS" -r 30 p1-240fps-sp128-slow.mp4
ffmpeg -i p1-240fps-sp64.mp4  -vf "setpts=8*PTS" -r 30 p1-240fps-sp64-slow.mp4
ffmpeg -i p1-240fps-sp256.mp4 -vf "setpts=8*PTS" -r 30 p1-240fps-sp256-slow.mp4

ffmpeg -i p03-240fps-sp256.mp4 -vf "setpts=8*PTS" -r 30 p03-240fps-sp256-slow.mp4
ffmpeg -i p07-240fps-sp256.mp4 -vf "setpts=8*PTS" -r 30 p07-240fps-sp256-slow.mp4




# cut out - no re-encoding
ffmpeg -i p01.mp4 -ss 00:00:00 -to 00:00:02 -c copy p01-1.mp4

# cut out -    re-encoding
ffmpeg -i p01.mp4 -ss 00:00:00     -to 00:00:02.500         p01-segment.mp4
ffmpeg -i p02.mp4 -ss 00:00:00.300 -to 00:00:02.825         p02-segment.mp4
ffmpeg -i p02a.mp4 -ss 00:00:00    -to 00:00:02.500         p02a-segment.mp4
ffmpeg -i p03.mp4 -ss 00:00:00     -to 00:00:02.500         p03-segment.mp4
ffmpeg -i p05.mp4 -ss 00:00:00     -to 00:00:06.500         p05-segment.mp4
ffmpeg -i p06.mp4 -ss 00:00:00     -to 00:00:01.400         p06-segment.mp4
ffmpeg -i p07.mp4 -ss 00:00:00.267 -to 00:00:03.871         p07-segment.mp4
ffmpeg -i p08.mp4 -ss 00:00:01.605 -to 00:00:05.711         p08-segment.mp4
ffmpeg -i p09.mp4 -ss 00:00:00.500 -to 00:00:05.906         p09-segment.mp4
ffmpeg -i p11.mp4 -ss 00:00:00.500          p11-segment.mp4


ffmpeg -i p07-slow.mp4 -ss 00:00:00.000 -to 00:00:03.200         p07-slow-segment-1.mp4
ffmpeg -i p07-slow.mp4 -ss 00:00:17.000 -to 00:00:22.500         p07-slow-segment-2.mp4



# re encode - to have b-frames
#     - -crf  0 -           no compression
#     - -crf 18 - virtually no compression
ffmpeg -i p07.mp4 -c:v libx264 -crf 18 -preset slow -c:a copy p07-re-encoded.mp4
ffmpeg -i p08.mp4 -c:v libx264 -crf 18 -preset slow -c:a copy p08-re-encoded.mp4






## H.265 to H.264 for DaVinci Resolve
ffmpeg -i p1.mp4 -map 0 -c:v libx264 -crf 18 -vf format=yuv420p -c:a copy p1-8bit.mkv


