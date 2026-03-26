#!/usr/bin/env python3

import sys
import os
import tempfile
import shutil
import json
import math
from   pathlib  import Path
from   lib.util import stackTrace

from   PIL import Image
import imagehash
import jinja2


import ffmpeg
#  alternative
#  https://github.com/mkan1ewski/pyffmpeg

# slim wrapper
#  https://pypi.org/project/ffmpy/


investigateSeconds = 10*60

# 10 is very sensitive
phashJumpThreshold = 10

# 20 still captures most changes
phashJumpThreshold = 20

# beyond 20 - indiscriminate reductions appear

# 15 is a good baseline to drop visually similar scenes (e.g. A-B-A interview cuts)
phashSimilarityThreshold = 25


# work dir - or default ".s"
dirArg  = sys.argv[1] if len(sys.argv) > 1 else "."
dirPath = Path(dirArg)

templatePath = Path("list-template.html")
if not templatePath.exists():
    print(f"Template not found: {templatePath}")
    sys.exit(-1)

with open(templatePath, "r", encoding="utf-8") as f:
    templateContent = f.read()
jinjaTemplate = jinja2.Template(templateContent)


workSpace = dirPath / ".thumbs"  /"~frames"
os.makedirs( workSpace,exist_ok=True )

# workSpace = Path(tempfile.mkdtemp())

print(f"creating movie thumbs for dir {dirPath} - wsp {workSpace}")

try:
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
      outHsh = baseName.parent/ ".thumbs" / f"{baseName.name}-phashes.json"

      print(f"processing: {fn}")

      hashData = []
      if outHsh.exists():
          print(f"\tphashes exist {outHsh}")
          with open(outHsh, "r") as f:
              hashData = json.load(f)
      else:
          print(f"\tphashes new for {fn}")
          probe = ffmpeg.probe(str(fn))
          videoStream = None
          for idx2, stream in enumerate(probe['streams']):
              if stream['codec_type'] == 'video':
                  videoStream = stream
                  break

          fps = 25.0
          if videoStream is not None:
              if 'r_frame_rate' in videoStream:
                  fpsParts = videoStream['r_frame_rate'].split('/')
                  if len(fpsParts) == 2:
                      num = float(fpsParts[0])
                      den = float(fpsParts[1])
                      if den > 0:
                          fps = num / den

          print(f"\t  fps detection {fps}")

          hashWorkDir = Path(tempfile.mkdtemp(dir=workSpace, prefix="hashframes."))
          (
              ffmpeg
              .input( str(fn), t=investigateSeconds)
              .output(str(hashWorkDir / "frame_%05d.jpg"), vf="scale=160:-2", qscale=5)
              .overwrite_output()
              .run(quiet=True)
          )

          extractedFiles = []
          for idx2, frameFile in enumerate(hashWorkDir.glob("frame_*.jpg")):
              extractedFiles.append(frameFile)
          extractedFiles.sort()

          for idx2, frameFile in enumerate(extractedFiles):
              if idx2 % 325 == 0:
                  print(f"\t  phash for frame {idx2:5} ")

              img = Image.open(frameFile)
              h = str(imagehash.phash(img))
              timeOffset = idx2 / fps
              hashData.append({"frame": idx2, "hash": h, "time": timeOffset})

          with open(outHsh, "w") as f:
              json.dump(hashData, f, indent=2)

          shutil.rmtree(hashWorkDir, ignore_errors=True)

      cutPoints = [0.0]
      last10Dists = []

      for idx2, data in enumerate(hashData):
          if idx2 == 0:
              continue

          prevHash = imagehash.hex_to_hash(hashData[idx2-1]["hash"])
          currHash = imagehash.hex_to_hash(data["hash"])
          dist = currHash - prevHash

          sumDist = 0.0
          for idx3, d in enumerate(last10Dists):
              sumDist += d
          avgDist = sumDist / len(last10Dists) if len(last10Dists) > 0 else 0.0

          if dist - avgDist > phashJumpThreshold:
              cutPoints.append(data["time"])

          last10Dists.append(dist)
          if len(last10Dists) > 10:
              last10Dists.pop(0)

      if len(hashData) > 0:
          cutPoints.append(hashData[-1]["time"])
      else:
          cutPoints.append(investigateSeconds)

      tsList = []
      for idx2, cut in enumerate(cutPoints):
          if idx2 == 0:
              continue
          prevCut = cutPoints[idx2-1]
          midpoint = prevCut + (cut - prevCut) / 2.0
          tsList.append(midpoint)

      if len(tsList) == 0:
          tsList = [0, 10, 20, 30]

      filteredTsList = []
      acceptedHashes = []

      for idx2, t in enumerate(tsList):
          closestFrameData = None
          minTimeDiff = 999999.0
          for idx3, data in enumerate(hashData):
              timeDiff = abs(data["time"] - t)
              if timeDiff < minTimeDiff:
                  minTimeDiff = timeDiff
                  closestFrameData = data

          if closestFrameData is not None:
              currHash = imagehash.hex_to_hash(closestFrameData["hash"])
              isDistinct = True
              for idx3, accHash in enumerate(acceptedHashes):
                  dist = currHash - accHash
                  if dist < phashSimilarityThreshold:
                      isDistinct = False
                      break

              if isDistinct:
                  filteredTsList.append(t)
                  acceptedHashes.append(currHash)

      if len(filteredTsList) == 0:
          if len(tsList) > 0:
              filteredTsList.append(tsList[0])
          else:
              filteredTsList = [0, 10, 20, 30]

      tsList = filteredTsList

      workDir = Path(tempfile.mkdtemp(dir=workSpace, prefix="frames."))

      # extract frames
      #     seek before -i for faster, accurate cuts
      for idx2, t in enumerate(tsList):
        numStr = f"{idx2:04d}"
        frameOut = workDir / f"frame_{numStr}.png"
        
        hh      = int(t // 3600)
        mm      = int((t % 3600) // 60)
        ss      = int(t % 60)
        timeStr = f"{hh:02d}\\:{mm:02d}\\:{ss:02d}"
        
        vfStr = f"scale=1600:-2,drawtext=text='{timeStr}':x=w-tw-20:y=h-th-20:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.6"
        
        (
            ffmpeg
            .input(str(fn), ss=t)
            .output(str(frameOut), vframes=1, vf=vfStr)
            .overwrite_output()
            .run(quiet=True)
        )


      # dynamic grid from N frames
      cols = math.ceil(math.sqrt(len(tsList)))
      rows = math.ceil(len(tsList) / cols) if cols > 0 else 1
      tileStr = f"tile={cols}x{rows}:padding=10:margin=10,format=rgb24,scale=1600:-2"

      frameInput = str(workDir / "frame_%04d.png")
      (
          ffmpeg
          .input(frameInput, framerate=1)
          .output(str(outPng), vf=tileStr, vframes=1)
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


      print(f"\twrote: {outPng}")
      print(f"\twrote: {outWbp}")

      htmlOut = baseName.parent / ".thumbs" / f"{baseName.name}.html"

      # Series of 2x2 tiles
      chunkSize = 4
      numChunks = math.ceil(len(tsList) / chunkSize)
      
      chunkList = []
      for idx2 in range(numChunks):
          chunkList.append(idx2)
          
      chunksData = []
          
      for idx2, chunkIdx in enumerate(chunkList):
          chunkDir = workDir / f"chunk_{chunkIdx:03d}"
          chunkDir.mkdir(parents=True, exist_ok=True)
          
          chunkFrames = []
          for idx3, t in enumerate(tsList):
              if idx3 >= chunkIdx * chunkSize and idx3 < (chunkIdx + 1) * chunkSize:
                  chunkFrames.append(t)
                  
          for idx3, t in enumerate(chunkFrames):
              srcIdx = chunkIdx * chunkSize + idx3
              srcFrame = workDir  / f"frame_{srcIdx:04d}.png"
              dstFrame = chunkDir / f"frame_{idx3:04d}.png"
              shutil.copy(srcFrame, dstFrame)
              
          chunkFrameInput = str(chunkDir / "frame_%04d.png")
          outPngChunk = baseName.parent / ".thumbs" / f"{baseName.name}-thumb-{chunkIdx+1:03d}.png"
          
          cCols = 2
          cRows = math.ceil(len(chunkFrames) / cCols) if cCols > 0 else 1
          cTileStr = f"tile={cCols}x{cRows}:padding=10:margin=10,format=rgb24,scale=1600:-2"
          
          (
              ffmpeg
              .input(chunkFrameInput, framerate=1)
              .output(str(outPngChunk), vf=cTileStr, vframes=1)
              .overwrite_output()
              .run(quiet=True)
          )
          print(f"\twrote: {outPngChunk}")

          chunkDict = {
              "image": outPngChunk.name,
              "links": []
          }
          
          for idx3, t in enumerate(chunkFrames):
              hh = int(t // 3600)
              mm = int((t % 3600) // 60)
              ss = int(t % 60)
              displayTime = f"{hh:02d}:{mm:02d}:{ss:02d}"
              
              # mpv command line syntax: mpv --start=12.34 "../video.mp4"
              # Custom protocol link format. Requires OS registry configuration to pass arguments to mpv.exe
              fileUri = fn.resolve().as_uri()
              link = f"mpv://--start={t}/{fileUri}"
              
              chunkDict["links"].append({
                  "url": link,
                  "displayTime": displayTime
              })
              
          chunksData.append(chunkDict)

      htmlRendered = jinjaTemplate.render(baseName=baseName.name, chunks=chunksData)
      
      with open(htmlOut, "w", encoding="utf-8") as f:
          f.write(htmlRendered)
      print(f"\twrote: {htmlOut}")

except Exception as exc:
    stackTrace(exc)
    sys.exit(-1)
finally:
    pass
    # shutil.rmtree(workSpace, ignore_errors=True)
