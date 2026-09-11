"""
    any mkv file gets prepended and appended with a still image

"""
import sys
import subprocess
from pathlib import Path

try:
    from lib.util import stackTrace
except ImportError:
    def stackTrace(exc):
        pass


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
        stackTrace(exc)
        print("[hasAudioStream] Exception while probing audio stream")
        return False

    if probeOut.strip() == "":
        return False

    return True


def getVideoResolution(
    inpPth
):

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
        width, height = probeOut.split(",")
        return width, height
    except Exception as exc:
        stackTrace(exc)
        print("[getVideoResolution] Exception while probing resolution")
        sys.exit(-1)


def prependImage(
    inpPth,
    imgPth,
    outPth,
    durationSec,
):

    width, height = getVideoResolution(inpPth)
    audioExists = hasAudioStream(inpPth)

    if audioExists:
        ffmpegCmd = [
            "ffmpeg",
            "-y",
            # looping the still image for the specified duration
            "-loop", "1",
            "-t", f"{durationSec}",
            "-i", str(imgPth),
            "-i", str(inpPth),
            # generating silent audio to match the video's audio stream during the image display
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex",
            (
                # scaling and padding the image to fit the video resolution exactly without stretching
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,format=yuv420p[imgv];"
                # concatenating image+silence with the main video+audio
                f"[imgv][2:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]"
            ),
            "-map", "[v]",
            "-map", "[a]",

            # high quality
            "-c:v",        "libx264",
            "-level",      "6.2",
            "-crf",        "18",
            "-preset",     "slow",
            "-g",          "1",
            "-bf",         "0",
            "-keyint_min", "1",
            "-vsync",      "cfr",

            str(outPth)
        ]

    else:
        ffmpegCmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-t", f"{durationSec}",
            "-i", str(imgPth),
            "-i", str(inpPth),
            "-filter_complex",
            (
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,format=yuv420p[imgv];"
                # concatenating only video streams since no audio exists
                f"[imgv][1:v]concat=n=2:v=1:a=0[v]"
            ),
            "-map", "[v]",

            # high quality
            "-c:v",        "libx264",
            "-level",      "6.2",
            "-crf",        "18",
            "-preset",     "slow",
            "-g",          "1",
            "-bf",         "0",
            "-keyint_min", "1",
            "-vsync",      "cfr",

            str(outPth)
        ]

    try:
        subprocess.run(ffmpegCmd, check=True)
    except Exception as exc:
        stackTrace(exc)
        print("[prependImage] Exception while running ffmpeg")
        sys.exit(-1)


def appendImage(
    inpPth,
    imgPth,
    outPth,
    durationSec
):

    width, height = getVideoResolution(inpPth)
    audioExists = hasAudioStream(inpPth)

    if audioExists:
        ffmpegCmd = [
            "ffmpeg",
            "-y",
            "-i", str(inpPth),
            "-loop", "1",
            "-t", f"{durationSec}",
            "-i", str(imgPth),
            "-f", "lavfi",
            "-t", f"{durationSec}",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex",
            (
                f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,format=yuv420p[imgv];"
                f"[0:v][0:a][imgv][2:a]concat=n=2:v=1:a=1[v][a]"
            ),
            "-map", "[v]",
            "-map", "[a]",

            # high quality
            "-c:v",        "libx264",
            "-level",      "6.2",
            "-crf",        "18",
            "-preset",     "slow",
            "-g",          "1",
            "-bf",         "0",
            "-keyint_min", "1",
            "-vsync",      "cfr",

            str(outPth)
        ]

    else:
        ffmpegCmd = [
            "ffmpeg",
            "-y",
            "-i", str(inpPth),
            "-loop", "1",
            "-t", f"{durationSec}",
            "-i", str(imgPth),
            "-filter_complex",
            (
                f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,format=yuv420p[imgv];"
                f"[0:v][imgv]concat=n=2:v=1:a=0[v]"
            ),
            "-map", "[v]",
            "-map", "0:a?",

            # high quality
            "-c:v",        "libx264",
            "-level",      "6.2",
            "-crf",        "18",
            "-preset",     "slow",
            "-g",          "1",
            "-bf",         "0",
            "-keyint_min", "1",
            "-vsync",      "cfr",

            str(outPth)
        ]

    try:
        subprocess.run(ffmpegCmd, check=True)
    except Exception as exc:
        stackTrace(exc)
        print("[appendImage] Exception while running ffmpeg")
        sys.exit(-1)


if __name__ == "__main__":

    inpF = Path("p1.mkv")
    imgPrepend = Path("intro.jpg")
    imgAppend  = Path("outro.jpg")

    if not inpF.exists():
        print(f"Input video not found: {inpF}")
        sys.exit(-1)

    outF1 = inpF.with_name(inpF.stem + "-1-img-prepend" + inpF.suffix)
    outF2 = inpF.with_name(inpF.stem + "-2-img-append"  + inpF.suffix)

    if imgPrepend.exists():
        prependImage(
            inpF,
            imgPrepend,
            outF1,
            1.4,
        )
    else:
        print(f"Prepend image not found: {imgPrepend}")

    if imgAppend.exists():
        # using outF1 as input if prepend succeeded, otherwise fallback to inpF
        srcForAppend = outF1 if outF1.exists() else inpF
        appendImage(
            srcForAppend,
            imgAppend,
            outF2,
            3.5,
        )
    else:
        print(f"Append image not found: {imgAppend}")