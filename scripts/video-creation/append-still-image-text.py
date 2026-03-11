"""
    any mkv file gets appended with a still image

    black background
    white text

    3 seconds

"""
from pathlib import Path
import subprocess

def addBlackWithText(
        inputPath, 
        outputPath, 
        userText
):

    fontPath = Path("./fonts/GothicA1-Regular.ttf")

    # probe resolution
    probeCmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        str(inputPath)
    ]

    try:
        probeOut = subprocess.check_output(probeCmd).decode().strip()
    except Exception as exc:
        print(f"Exception while probing resolution: {exc}")
        return

    width, height = probeOut.split(",")

    # build ffmpeg command
    ffmpegCmd = [
        "ffmpeg",
        "-i", str(inputPath),
        "-f", "lavfi",
        "-t", "3",
        "-i", f"color=size={width}x{height}:rate=30:color=black",
        "-filter_complex",
        (
            f"[1:v]drawtext=fontfile='{fontPath}':fontcolor=white:fontsize=72:"
            f"text='{userText}':"
            f"text_align=center:"
            f"line_spacing=16:"      # in pixels - in addition to font-size            
            f"x=(w-text_w)/2:y=(h-text_h)/2,"
            f"format=yuv420p[black];"
            f"[0:v][black]concat=n=2:v=1:a=0[v]"
        ),
        "-map", "[v]",
        "-map", "0:a?",
        str(outputPath)
    ]

    try:
        subprocess.run(ffmpegCmd, check=True)
    except Exception as exc:
        print(f"Exception while running ffmpeg: {exc}")


inpF = Path("input.mkv")

# Example:
addBlackWithText(
    inpF,
    inpF.with_name( inpF.stem + "_text" + inpF.suffix ), 
    "Now?\n(while your parents are next room)\nOr tomorrow?"
)
