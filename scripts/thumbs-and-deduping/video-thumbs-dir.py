#!/usr/bin/env python3


import sys
import os
import tempfile
import shutil
from   pathlib  import Path
from   lib.util import stackTrace


import ffmpeg
#  alternative
#  https://github.com/mkan1ewski/pyffmpeg

# slim
#  https://pypi.org/project/ffmpy/


# work dir - or default ".s"
dirArg  = sys.argv[1] if len(sys.argv) > 1 else "."
dirPath = Path(dirArg)


print(f"creating movie thumbs for dir {dirPath}")

workSpace = Path(tempfile.mkdtemp())

try:
    # four timestamps: 0s,10s,20s,30s
    tsList = [0, 10, 20, 30]

    videoFiles = []
    for idx1, fn in enumerate(dirPath.iterdir()):
        if fn.is_file() and fn.suffix.lower() in [".mkv", ".mp4"]:
            videoFiles.append(fn)

    for idx1, fn in enumerate(videoFiles):
      
      # skip if the glob didn't match anything
      if not fn.exists():
          print(f"File not found: {fn}")
          sys.exit(-1)

      baseName = fn.with_suffix("")
      os.makedirs(baseName.parent/ ".thumbs",exist_ok=True )

      outPng = baseName.parent/ ".thumbs" / f"{baseName.name}-thumb.png"
      outWbp = baseName.parent/ ".thumbs" / f"{baseName.name}-thumb.webp"

      print(f"processing: {fn}")
      workDir = Path(tempfile.mkdtemp(dir=workSpace, prefix="frames."))

      # extract frames 
      #     seek before -i for faster, accurate cuts
      for idx2, t in enumerate(tsList):
        numStr = f"{idx2:02d}"
        frameOut = workDir / f"frame_{numStr}.png"
        (
            ffmpeg
            .input(str(fn), ss=t)
            .output(str(frameOut), vframes=1, vf="scale=320:-2")
            .overwrite_output()
            .run(quiet=True)
        )


      # 2x2 grid from 4 frames
      frameInput = str(workDir / "frame_%02d.png")
      (
          ffmpeg
          .input(frameInput, framerate=1)
          .output(str(outPng), vf="tile=2x2:padding=10:margin=10,format=rgb24", vframes=1)
          .overwrite_output()
          .run(quiet=True)
      )


      # Animated WebP (1 fps, loop forever)
      (
          ffmpeg
          .input(frameInput, framerate=1)
          .output(str(outWbp), vf="format=rgba", loop=0, vcodec="libwebp", **{"q:v": 70, "compression_level": 6})
          .overwrite_output()
          .run(quiet=True)
      )


      print(f"\twrote: {outPng}, {outWbp}")

except Exception as exc:
    stackTrace(exc)
    sys.exit(-1)
finally:
    shutil.rmtree(workSpace, ignore_errors=True)
