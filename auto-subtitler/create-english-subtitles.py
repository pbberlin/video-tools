# pip install openai-whisper
from pathlib import Path
import subprocess
import whisper

def extractAudio(inputVideoPath, outputAudioPath):
    command = [
        "ffmpeg",
        "-i", str(inputVideoPath),
        "-vn",
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(outputAudioPath)
    ]

    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        print("FFmpeg error:")
        print(process.stderr)
    else:
        print("Audio extracted:", outputAudioPath)


def runWhisper(
        audioPath, 
        modelName="medium",
):

    print("Loading Whisper model:", modelName)
    model = whisper.load_model(modelName)

    print("Transcribing...")
    result = model.transcribe(
        str(audioPath),
        task="translate",
        language="cs"
    )
    return result


def writeSrt(result, outputSrtPath):
    lines = result["segments"]
    with open(outputSrtPath, "w", encoding="utf-8") as srtFile:
        for lineIndex in range(len(lines)):
            segment = lines[lineIndex]

            sttTime = segment["start"]
            endTime = segment["end"]
            text    = segment["text"].strip()

            sttSrt = formatTimestamp(sttTime)
            endSrt = formatTimestamp(endTime)

            srtFile.write(str(lineIndex + 1) + "\n")
            srtFile.write(sttSrt + " --> " + endSrt + "\n")
            srtFile.write(text + "\n\n")

    print("Saved subtitles to:", outputSrtPath)


def formatTimestamp(secondsFloat):
    hrs = int(secondsFloat // 3600)
    mns = int((secondsFloat % 3600) // 60)
    scs = int(secondsFloat % 60)
    ms  = int((secondsFloat % 1) * 1000)

    timestamp = f"{hrs:02d}:{mns:02d}:{scs:02d},{ms:03d}"
    return timestamp


def main():
    inpPth    = Path("a.mp4")
    audioPth  = Path("audio.wav")
    outSrtPth = Path("a.srt")

    extractAudio(inpPth, audioPth)

    result = runWhisper(
        audioPth, 
        modelName="medium",
        # modelName="large",
    )
    writeSrt(result, outSrtPth)


if __name__ == "__main__":
    main()
