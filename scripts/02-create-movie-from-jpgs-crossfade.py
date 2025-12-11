import subprocess
from pathlib import Path

# ---------- Settings ----------
targetWidth  = 1920
targetHeight = 1080
secondsPerImage = 1.8
blendDuration = 0.2
outputFps = 25
outputFile = "slideshow-crossfade.mp4"
# ------------------------------

def collectJpgsSorted():
    cwd = Path.cwd()
    jpgFiles = []

    for pattern in ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]:
        for p in cwd.glob(pattern):
            jpgFiles.append(p)

    # Sort by filename (case-insensitive)
    jpgFiles = sorted(jpgFiles, key=lambda x: x.name.lower())
    return jpgFiles

def buildFfmpegCommand(files):
    if len(files) == 0:
        print("No JPG/JPEG images found.")
        return None

    cmd = []
    cmd.append("ffmpeg")
    cmd.append("-y")

    index = 0
    for f in files:
        cmd.append("-loop")
        cmd.append("1")
        cmd.append("-t")
        cmd.append(f"{secondsPerImage}")
        cmd.append("-i")
        cmd.append(str(f))
        index += 1

    filterLines = []

    i = 0
    for _ in files:
        # Build WITHOUT a comma after the input label.
        # Correct: [i:v]scale=...,pad=...,setsar=1[s{i}]
        scalePart = f"scale={targetWidth}:{targetHeight}:force_original_aspect_ratio=decrease"
        padPart = f"pad={targetWidth}:{targetHeight}:(ow-iw)/2:(oh-ih)/2:black"
        line = f"[{i}:v]{scalePart},{padPart},setsar=1[s{i}]"
        filterLines.append(line)
        i += 1

    if len(files) == 1:
        lastLabel = "[s0]"
    else:
        k = 1
        prevLabel = "[s0]"
        nextIndex = 1
        while nextIndex < len(files):
            currLabel = f"[s{nextIndex}]"
            outLabel = f"[x{k}]"

            offsetValue = (k * secondsPerImage) - (k * blendDuration)
            offsetStr = f"{offsetValue:.6f}".rstrip("0").rstrip(".")

            # Correct xfade chain syntax: [A][B]xfade=... [OUT]
            xfadeLine = (
                f"{prevLabel}{currLabel}"
                f"xfade=transition=fade:duration={blendDuration}:offset={offsetStr} {outLabel}"
            )
            filterLines.append(xfadeLine)

            prevLabel = outLabel
            k += 1
            nextIndex += 1

        lastLabel = prevLabel

    finalOutLabel = "[vout]"
    filterLines.append(f"{lastLabel}format=yuv420p,setsar=1{finalOutLabel}")

    filterComplex = "; ".join(filterLines)

    cmd.append("-filter_complex")
    cmd.append(filterComplex)

    cmd.append("-map")
    cmd.append(finalOutLabel)

    cmd.append("-r")
    cmd.append(f"{outputFps}")

    cmd.append("-movflags")
    cmd.append("+faststart")

    cmd.append("-pix_fmt")
    cmd.append("yuv420p")

    cmd.append(outputFile)

    return cmd

def runFfmpeg(cmd):
    if cmd is None:
        return
    print("Running ffmpeg command:")
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed with exit code {e.returncode}")
        print(e)

def main():
    files = collectJpgsSorted()
    print(f"Found {len(files)} image(s).")
    cmd = buildFfmpegCommand(files)
    runFfmpeg(cmd)
    if cmd is not None:
        print(f"Done. Wrote {outputFile}")

if __name__ == "__main__":
    main()
