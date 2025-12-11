from pathlib import Path
import subprocess
import json
import math
import shlex
import sys

def getVideoDurationSeconds(inputPath):
    try:
        cmd = []
        cmd.append("ffprobe")
        cmd.append("-v")
        cmd.append("error")
        cmd.append("-select_streams")
        cmd.append("v:0")
        cmd.append("-show_entries")
        cmd.append("format=duration")
        cmd.append("-of")
        cmd.append("json")
        cmd.append(str(inputPath))

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        durationStr = data.get("format", {}).get("duration", None)
        if durationStr is None:
            raise RuntimeError("Could not read duration with ffprobe.")
        duration = float(durationStr)
        return duration
    except Exception as e:
        print("Failed to read duration via ffprobe.")
        print(e)
        raise

def buildDrawtextVfChain(
    nSlides,
    secondsPerImage,
    blendDuration,
    fontPath,
    fontSize,
    fontColor,
    borderColor,
    borderWidth,
    xOffset,
    yOffset,
    endCap=None
):
    try:
        vfParts = []

        # For slide i (0-based):
        # fully visible window (excluding blends) is
        #   start = i*secondsPerImage + blendDuration
        #   end   = (i+1)*secondsPerImage - blendDuration
        #
        # This hides the counter during both the incoming and outgoing xfade.
        # For the first and last slide, this simply shortens the window a bit, which is fine.

        i = 0
        while i < nSlides:
            textValue = str(i + 1)

            startT = (i * secondsPerImage) + blendDuration
            endT = ((i + 1) * secondsPerImage) - blendDuration

            if endCap is not None:
                if startT > endCap:
                    break
                if endT > endCap:
                    endT = endCap

            # Skip invalid windows (can happen on very short clips)
            if endT > startT:
                # Right-aligned, bottom-right:
                # x = w - text_w - xOffset
                # y = h - text_h - yOffset
                part = (
                    "drawtext="
                    f"text='{textValue}':"
                    f"fontfile={fontPath}:"
                    f"fontcolor={fontColor}:"
                    f"fontsize={int(fontSize)}:"
                    f"x=w-text_w-{int(xOffset)}:"
                    f"y=h-text_h-{int(yOffset)}:"
                    f"bordercolor={borderColor}:"
                    f"borderw={int(borderWidth)}:"
                    f"enable='between(t,{startT:.3f},{endT:.3f})'"
                )
                vfParts.append(part)

            i = i + 1

        # Join with commas (single -vf chain)
        vfChain = ""
        j = 0
        while j < len(vfParts):
            if j == 0:
                vfChain = vfParts[j]
            else:
                vfChain = vfChain + "," + vfParts[j]
            j = j + 1

        return vfChain
    except Exception as e:
        print("Failed to build drawtext filter chain.")
        print(e)
        raise

def buildFfmpegCommand(
    inputMp4Path,
    outputMp4Path,
    vfChain,
    outputFps
):
    try:
        cmd = []
        cmd.append("ffmpeg")
        cmd.append("-y")
        cmd.append("-i")
        cmd.append(str(inputMp4Path))
        cmd.append("-vf")
        cmd.append(vfChain)
        cmd.append("-map")
        cmd.append("0:v:0")
        cmd.append("-map")
        cmd.append("0:a?")
        cmd.append("-r")
        cmd.append(str(int(outputFps)))
        cmd.append("-c:v")
        cmd.append("libx264")
        cmd.append("-crf")
        cmd.append("18")
        cmd.append("-pix_fmt")
        cmd.append("yuv420p")
        cmd.append("-movflags")
        cmd.append("+faststart")
        cmd.append(str(outputMp4Path))
        return cmd
    except Exception as e:
        print("Failed to build ffmpeg command.")
        print(e)
        raise

def main():
    try:
        # ---- Your fixed settings ----
        targetWidth  = 1920
        targetHeight = 1080
        
        """       
            function of value 'secondsPerImage' in  02-create-movie-from-jpgs-crossfade.py
                1.2 => 2.4
                1.8 => 3.2


        """       
        secondsPerImage = 2.4  
        secondsPerImage = 3.2  
        blendDuration   = 0.2
        
        outputFps = 25

        inputMp4  = Path("slideshow-crossfade.mp4")
        outputMp4 = Path("slideshow-crossfade-numbered.mp4")
        fontPath  = Path("./fonts/GothicA1-Regular.ttf")   # change if needed

        if not inputMp4.exists():
            raise FileNotFoundError(f"Input not found: {inputMp4}")

        if not fontPath.exists():
            raise FileNotFoundError(f"Font not found: {fontPath}")

        # ---- Probe duration ----
        duration = getVideoDurationSeconds(inputMp4)

        # ---- Derive number of slides ----
        # Typical xfade pipeline: total duration ≈ n*secondsPerImage + blendDuration
        # => n ≈ round((duration - blendDuration) / secondsPerImage)
        # Guard both ways with a small epsilon and floor
        est = (duration - blendDuration) / secondsPerImage
        if est < 1:
            est = 1
        nSlides = int(math.floor(est + 0.5))
        if nSlides < 1:
            nSlides = 1

        # Cap any per-slide windows that exceed the actual duration
        endCap = duration

        # ---- Build -vf chain ----
        vfChain = buildDrawtextVfChain(
            nSlides=nSlides,
            secondsPerImage=secondsPerImage,
            blendDuration=blendDuration,
            fontPath=fontPath.as_posix(),   # forward slashes for ffmpeg
            # fontSize=48,
            fontSize=64,
            fontColor="white",
            borderColor="white",
            borderWidth=2,
            # xOffset=20,
            xOffset=40,
            # yOffset=12,
            yOffset=24,
            endCap=endCap
        )

        if vfChain == "":
            raise RuntimeError("Empty drawtext chain. Check duration and settings.")

        # ---- Build command ----
        cmd = buildFfmpegCommand(
            inputMp4Path=inputMp4,
            outputMp4Path=outputMp4,
            vfChain=vfChain,
            outputFps=outputFps
        )

        # Print a Windows-friendly one-liner you can paste in cmd.exe
        printable = []
        k = 0
        while k < len(cmd):
            s = str(cmd[k])
            # Double % for cmd.exe safety (not strictly needed here, but harmless)
            s = s.replace("%", "%%")
            # Quote parts that contain spaces, commas, colons, semicolons or quotes
            if (" " in s) or ("," in s) or (":" in s) or (";" in s) or ("'") in s:
                s = "\"" + s + "\""
            printable.append(s)
            k = k + 1

        print("FFmpeg command:")
        print(" ".join(printable))

        # If you want to run it immediately:
        subprocess.run(cmd, check=True)
        print(f"Done: {outputMp4}")

    except Exception as e:
        print("Failed.")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
