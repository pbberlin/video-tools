#  pip install openai-whisper requests
#  pip install openai

# DeepL (recommended): 
# export DEEPL_API_KEY="your_key_here"


from pathlib import Path
import subprocess
import whisper
import os
import re
import time
import openai
import requests
import os

isSet = os.getenv("OPENAI_API_KEY")

if isSet == "":
    print(f"must set env variable 'OPENAI_API_KEY'")
    os._exit(-1)



def extractAudio(inputVideoPath, outputAudioPath):
    print("Step 1/5: Extracting audio with ffmpeg...")
    command = [
        "ffmpeg",
        "-y",
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
        print("Audio extracted to:", outputAudioPath)


def transcribeCzechWhisper(audioPath, modelName="large"):
    print("Step 2/5: Loading Whisper model:", modelName)
    try:
        model = whisper.load_model(modelName)
    except Exception as e:
        print("Failed to load Whisper model:")
        print(e)
        raise

    print("Transcribing Czech (cs)...")
    try:
        result = model.transcribe(
            str(audioPath),
            task="transcribe",
            language="cs",
        )
        return result
    except Exception as e:
        print("Whisper transcription error:")
        print(e)
        raise


def formatTimestamp(secondsFloat):
    hours = int(secondsFloat // 3600)
    minutes = int((secondsFloat % 3600) // 60)
    seconds = int(secondsFloat % 60)
    milliseconds = int((secondsFloat % 1) * 1000)
    timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    return timestamp


def writeSrtFromSegments(segments, outputSrtPath):
    print("Step 3/5: Writing Czech SRT:", outputSrtPath)
    try:
        with open(outputSrtPath, "w", encoding="utf-8") as srtFile:
            for i in range(len(segments)):
                seg = segments[i]
                startSrt = formatTimestamp(seg["start"])
                endSrt = formatTimestamp(seg["end"])
                text = seg["text"].strip()

                srtFile.write(str(i + 1) + "\n")
                srtFile.write(startSrt + " --> " + endSrt + "\n")
                srtFile.write(text + "\n\n")
    except Exception as e:
        print("Failed to write SRT:")
        print(e)
        raise


def parseSrt(srtPath):
    # Returns a list of dicts with keys: index, start, end, text
    print("Parsing SRT for translation:", srtPath)
    entries = []
    try:
        with open(srtPath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print("Failed to read SRT:")
        print(e)
        raise

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "":
            i += 1
            continue

        indexVal = None
        try:
            indexVal = int(line)
        except Exception as e:
            # Not a standard index line; try to continue parsing but report
            print("Non-integer index encountered at line", i + 1)
            print(e)

        i += 1
        if i >= len(lines):
            break

        timingLine = lines[i].strip()
        i += 1

        startStr = ""
        endStr = ""
        try:
            match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", timingLine)
            if match is not None:
                startStr = match.group(1)
                endStr = match.group(2)
            else:
                print("Malformed timing line near index", indexVal, ":", timingLine)
        except Exception as e:
            print("Failed to parse timing line:")
            print(e)

        textLines = []
        while i < len(lines) and lines[i].strip() != "":
            textLines.append(lines[i].rstrip("\n"))
            i += 1

        # Skip blank separator
        while i < len(lines) and lines[i].strip() == "":
            i += 1

        textJoined = ""
        # Prefer join when appropriate, per your guideline
        textJoined = "\n".join(textLines)

        entry = {
            "index": indexVal,
            "start": startStr,
            "end": endStr,
            "text": textJoined
        }
        entries.append(entry)

    return entries


def translateEntriesDeepL(csEntries, apiKey, formality="default", sleepSeconds=0.0):
    print("Step 4/5: Translating with DeepL...")
    url = "https://api-free.deepl.com/v2/translate"
    enTexts = []

    for i in range(len(csEntries)):
        czText = csEntries[i]["text"]
        try:
            payload = {
                "auth_key": apiKey,
                "text": czText,
                "source_lang": "CS",
                "target_lang": "EN",
            }
            if formality != "default":
                payload["formality"] = formality

            response = requests.post(url, data=payload, timeout=60)
            if response.status_code != 200:
                print("DeepL HTTP error for index", csEntries[i]["index"], "status:", response.status_code)
                print(response.text)
                enTexts.append("[DeepL error]")
            else:
                data = response.json()
                if "translations" in data and len(data["translations"]) > 0:
                    enTexts.append(data["translations"][0]["text"])
                else:
                    print("DeepL unexpected payload for index", csEntries[i]["index"])
                    print(data)
                    enTexts.append("[DeepL parse error]")
        except Exception as e:
            print("DeepL request failed at index", csEntries[i]["index"])
            print(e)
            enTexts.append("[DeepL request exception]")
        if sleepSeconds > 0.0:
            time.sleep(sleepSeconds)

    return enTexts


def translateEntriesOpenAI(csEntries, modelName="gpt-4o-mini", temperature=0.2, sleepSeconds=0.0):
    print("Step 4/5: Translating with OpenAI...")
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY", "")
    except Exception as e:
        print("OpenAI setup failed:")
        print(e)
        raise

    enTexts = []
    for i in range(len(csEntries)):
        czText = csEntries[i]["text"]
        prompt = (
            "Translate the following Czech subtitle text into natural, fluent English. "
            "Keep line breaks where they are. Do not add commentary. Only return the translation.\n\n"
            f"Czech:\n{czText}\n\nEnglish:"
        )

        try:
            resp = openai.ChatCompletion.create(
                model=modelName,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": "You translate Czech to English for film subtitles. Keep meaning concise."},
                    {"role": "user", "content": prompt}
                ],
            )
            enText = resp["choices"][0]["message"]["content"].strip()
            enTexts.append(enText)
        except Exception as e:
            print("OpenAI request failed at index", csEntries[i]["index"])
            print(e)
            enTexts.append("[OpenAI request exception]")
        if sleepSeconds > 0.0:
            time.sleep(sleepSeconds)

    return enTexts


def writeTranslatedSrt(csEntries, enTexts, outputSrtPath):
    print("Step 5/5: Writing English SRT:", outputSrtPath)
    if len(csEntries) != len(enTexts):
        print("Warning: entry count mismatch. Czech entries:", len(csEntries), "English lines:", len(enTexts))

    try:
        with open(outputSrtPath, "w", encoding="utf-8") as srtFile:
            for i in range(len(csEntries)):
                entry = csEntries[i]
                indexVal = entry["index"]
                if indexVal is None:
                    indexVal = i + 1

                srtFile.write(str(indexVal) + "\n")
                srtFile.write(entry["start"] + " --> " + entry["end"] + "\n")
                srtFile.write(enTexts[i] + "\n\n")
    except Exception as e:
        print("Failed to write translated SRT:")
        print(e)
        raise


def main():
    # Inputs / outputs
    inputVideoPath = Path("a.mp4")
    audioPath = Path("audio.wav")
    czechSrtPath = Path("a.cs.srt")
    englishSrtPath = Path("a.en.srt")

    # 1) Extract audio
    extractAudio(inputVideoPath, audioPath)

    # 2) Whisper Czech transcription
    result = transcribeCzechWhisper(audioPath, modelName="large")
    segments = result.get("segments", [])

    # 3) Write Czech SRT
    writeSrtFromSegments(segments, czechSrtPath)



    # 4) Translate Czech SRT -> English SRT (DeepL preferred; OpenAI fallback)
    csEntries = parseSrt(czechSrtPath)

    deeplKey  = os.environ.get("DEEPL_API_KEY",  "").strip()
    openaiKey = os.environ.get("OPENAI_API_KEY", "").strip()

    enTexts = []

    if len(deeplKey) > 0 and "requests" in globals():
        enTexts = translateEntriesDeepL(csEntries, apiKey=deeplKey, formality="default", sleepSeconds=0.0)
    elif len(openaiKey) > 0 and "openai" in globals():
        enTexts = translateEntriesOpenAI(csEntries, modelName="gpt-4o-mini", temperature=0.2, sleepSeconds=0.0)
    else:
        print("No translation API configured. Set DEEPL_API_KEY or OPENAI_API_KEY.")
        # Create a placeholder to keep pipeline consistent
        for i in range(len(csEntries)):
            placeholder = "[No translator configured] " + csEntries[i]["text"]
            enTexts.append(placeholder)

    # 5) Write English SRT using original timestamps
    writeTranslatedSrt(csEntries, enTexts, englishSrtPath)

    print("Done.")
    print("Czech SRT :", czechSrtPath)
    print("English SRT:", englishSrtPath)


if __name__ == "__main__":
    main()
