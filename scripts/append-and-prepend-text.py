"""
    any mkv file gets prepended and appended with text frames

"""
from   pathlib import Path
import subprocess




def normalizePathForFfmpeg(
    pth
):

    try:
        pth = pth.resolve()
    except Exception as exc:
        print(f"Exception while resolving path: {exc}")
        return str(pth)

    pthStr = pth.as_posix()

    # escape Windows drive colon for ffmpeg drawtext
    if len(pthStr) >= 2 and pthStr[1] == ":":
        pthStr = pthStr[0] + "\\:" + pthStr[2:]

    return pthStr


def getFontPath(
    fn
):

    localFontPath = Path("./fonts") / fn
    if localFontPath.exists():
        print(f"Found font file {fn} in subdir ./fonts")
        return localFontPath

    winFontsDir = Path("C:/Windows/Fonts")
    if winFontsDir.exists() is False:
        print(f"Fallback 1 - font file {fn} in subdir ./fonts")
        return localFontPath

    targetLower = fn.lower()

    try:
        for idx1, fontPth in enumerate(winFontsDir.iterdir()):
            if fontPth.is_file() is False:
                continue

            if fontPth.name.lower() == targetLower:
                print(f"Found font file {fn} in subdir 'C:/Windows/Fonts'  ")
                return fontPth

    except Exception as exc:
        print(f"Exception while searching Windows fonts: {exc}")
        return localFontPath


    print(f"Fallback 2 - font file {fn} in subdir ./fonts")
    return localFontPath




def hasAudioStream(
    inpPth
):

    probeCmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        str(inpPth)
    ]

    try:
        probeOut = subprocess.check_output(probeCmd).decode().strip()
    except Exception as exc:
        print(f"Exception while probing audio stream: {exc}")
        return False

    if probeOut.strip() == "":
        return False

    return True



def prependText(
    inpPth,
    outPth,
    userText,
    fontPath,
    durationSec,
):

    # probe resolution
    probeCmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        str(inpPth)
    ]

    try:
        probeOut = subprocess.check_output(probeCmd).decode().strip()
    except Exception as exc:
        print(f"Exception while probing resolution: {exc}")
        return

    width, height = probeOut.split(",")

    audioExists = hasAudioStream(inpPth)

    if audioExists:

        ffmpegCmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", f"color=size={width}x{height}:rate=30:color=black",
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-i", str(inpPth),
            "-filter_complex",
            (
                f"[0:v]drawtext=fontfile='{fontPath}':fontcolor=white:fontsize=72:"
                f"text='{userText}':"
                f"text_align=center:"
                f"line_spacing=16:"
                f"x=(w-text_w)/2:y=(h-text_h)/2,"
                f"format=yuv420p[blackv];"
                f"[blackv][1:a][2:v][2:a]concat=n=2:v=1:a=1[v][a]"
            ),
            "-map", "[v]",
            "-map", "[a]",
            str(outPth)
        ]

    else:

        ffmpegCmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", f"color=size={width}x{height}:rate=30:color=black",
            "-i", str(inpPth),
            "-filter_complex",
            (
                f"[0:v]drawtext=fontfile='{fontPath}':fontcolor=white:fontsize=72:"
                f"text='{userText}':"
                f"text_align=center:"
                f"line_spacing=16:"
                f"x=(w-text_w)/2:y=(h-text_h)/2,"
                f"format=yuv420p[blackv];"
                f"[blackv][1:v]concat=n=2:v=1:a=0[v]"
            ),
            "-map", "[v]",
            str(outPth)
        ]

    try:
        subprocess.run(ffmpegCmd, check=True)
    except Exception as exc:
        print(f"Exception while running ffmpeg: {exc}")





def appendText(
    inpPth,
    outPth,
    userText,
    fontPath,
    durationSec
):


    # probe resolution
    probeCmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        str(inpPth)
    ]

    try:
        probeOut = subprocess.check_output(probeCmd).decode().strip()
    except Exception as exc:
        print(f"Exception while probing resolution: {exc}")
        return

    width, height = probeOut.split(",")

    audioExists = hasAudioStream(inpPth)

    if audioExists:

        ffmpegCmd = [
            "ffmpeg",
            "-i", str(inpPth),
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", f"color=size={width}x{height}:rate=30:color=black",
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex",
            (
                f"[1:v]drawtext=fontfile='{fontPath}':fontcolor=white:fontsize=72:"
                f"text='{userText}':"
                f"text_align=center:"
                f"line_spacing=16:"
                f"x=(w-text_w)/2:y=(h-text_h)/2,"
                f"format=yuv420p[blackv];"
                f"[0:v][0:a][blackv][2:a]concat=n=2:v=1:a=1[v][a]"
            ),
            "-map", "[v]",
            "-map", "[a]",
            str(outPth)
        ]

    else:

        ffmpegCmd = [
            "ffmpeg",
            "-i", str(inpPth),
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", f"color=size={width}x{height}:rate=30:color=black",
            "-filter_complex",
            (
                f"[1:v]drawtext=fontfile='{fontPath}':fontcolor=white:fontsize=72:"
                f"text='{userText}':"
                f"text_align=center:"
                f"line_spacing=16:"
                f"x=(w-text_w)/2:y=(h-text_h)/2,"
                f"format=yuv420p[blackv];"
                f"[0:v][blackv]concat=n=2:v=1:a=0[v]"
            ),
            "-map", "[v]",
            "-map", "0:a?",
            str(outPth)
        ]

    try:
        subprocess.run(ffmpegCmd, check=True)
    except Exception as exc:
        print(f"Exception while running ffmpeg: {exc}")



# fontPathRaw = getFontPath("GothicA1-Regular.ttf")
fontPathRaw = getFontPath("MiriamMonoCLM-Book.ttf")
# fontPathRaw = getFontPath("arial.ttf")
fontPath    = normalizePathForFfmpeg(fontPathRaw)
print(f"font path is {fontPath}")



inpF = Path("input.mkv")

outF1 = inpF.with_name( inpF.stem + "-1-text-apppend" + inpF.suffix )
outF2 = inpF.with_name( inpF.stem + "-2-text-prepend" + inpF.suffix )


prependText(
    inpF,
    outF1, 
    "Nose is yearning\n\nfor excitement",
    fontPath,
    2.8,
)

appendText(
    outF1,
    outF2, 
    "She looks *almost* as\n\nhelpless as you.",
    fontPath,
    3.5,
)


