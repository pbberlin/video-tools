# Step 2
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


# I tried following motion estimation values;
#  but the result is all the same
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=ds'"            p01-120fps-meds.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=tss'"           p01-120fps-metss.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=tss'"           p01-120fps-metss.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=esa'"           p01-120fps-meesa.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:me=umh'"           p01-120fps-meumh.mp4


# we can expand from 30 fps to 120 fps - or to 240 fps
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'"                  p01-120fps.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240'"                  p01-240fps.mp4

# a higher value for search_param improves the quality (slow)
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120:search_param=128'" p01-120fps-sp128.mp4
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=128'" p01-240fps-sp128.mp4

# search_param=256 takes a long time - but is worth the wait
ffmpeg -i p01.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" p01-240fps-sp256.mp4
ffmpeg -i p02.mp4 -vf "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=240:search_param=256'" p02-240fps-sp256.mp4







# slo-mo - footage with high FPS to framerate to 30
# ============================

# The videos created above play 240 frames per second - extremely fast.
#   we want to slow this down to 30 fps - to get slow-mo



# -vf "setpts=4*PTS": slow down the video by a factor of 4. 
#                     setpts filter adjusts the Presentation Timestamp (PTS),
#                     which controls the timing of frames.
# 4*PTS:              Multiplies PTS by 4, effectively making video 4 times slower.
# -r 30:              setting output frame rate to 30 FPS.
ffmpeg -i p01-240fps-sp256.mp4 -vf "setpts=8*PTS" -r 30 p01-240fps-sp256-slow.mp4
ffmpeg -i p02-240fps-sp256.mp4 -vf "setpts=8*PTS" -r 30 p02-240fps-sp256-slow.mp4



