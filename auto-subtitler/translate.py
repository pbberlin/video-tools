from pathlib import Path
import os
import re

from openai import OpenAI

# Simple OpenAI translator for SRT (Czech -> English)
# Assumes: a.cs.srt exists. Produces: a.en.srt

def parseSrt(srtPath):
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
        # Skip blank lines
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        indexVal = None
        try:
            indexVal = int(lines[i].strip())
        except Exception as e:
            print("Non-integer index at line", i + 1)
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
                print("Malformed timing near index", indexVal, ":", timingLine)
        except Exception as e:
            print("Failed to parse timing line:")
            print(e)

        textLines = []
        while i < len(lines) and lines[i].strip() != "":
            textLines.append(lines[i].rstrip("\n"))
            i += 1

        # Skip blank separator(s)
        while i < len(lines) and lines[i].strip() == "":
            i += 1

        textJoined = "\n".join(textLines)

        entry = {
            "index": indexVal,
            "start": startStr,
            "end":   endStr,
            "text":  textJoined
        }
        entries.append(entry)

    return entries


def translateWithOpenAi(texts):

    apiKey = os.environ.get("OPENAI_API_KEY", "").strip()
    if len(apiKey) == 0:
        raise RuntimeError("OPENAI_API_KEY not set in environment.")

    client = OpenAI(api_key=apiKey)

    translations = []
    for i in range(len(texts)):
        czText = texts[i]
        prompt = (
            "Translate the following Czech subtitle text into concise, natural English. "
            "Preserve existing line breaks exactly. Return only the translation.\n\n"
            f"Czech:\n{czText}\n\nEnglish:"
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": "You translate Czech to English for film subtitles. Keep it faithful and natural; preserve line breaks."},
                    {"role": "user", "content": prompt}
                ],
            )
            outText = resp.choices[0].message.content.strip()
            translations.append(outText)
        except Exception as e:
            print("OpenAI request failed at item", i)
            print(e)
            translations.append("[OpenAI request failed]")
    return translations


def writeTranslatedSrt(entries, enTexts, outPath):
    if len(entries) != len(enTexts):
        print("Warning: count mismatch. Entries:", len(entries), "Translations:", len(enTexts))

    try:
        with open(outPath, "w", encoding="utf-8") as f:
            for i in range(len(entries)):
                idx = entries[i]["index"]
                if idx is None:
                    idx = i + 1
                f.write(str(idx) + "\n")
                f.write(entries[i]["start"] + " --> " + entries[i]["end"] + "\n")
                f.write(enTexts[i] + "\n\n")
    except Exception as e:
        print("Failed to write SRT:")
        print(e)
        raise


def main():
    inPath = Path("a.cs.srt")
    outPath = Path("a.en.srt")

    entries = parseSrt(inPath)

    texts = []
    for i in range(len(entries)):
        texts.append(entries[i]["text"])

    enTexts = translateWithOpenAi(texts)
    writeTranslatedSrt(entries, enTexts, outPath)

    print("Wrote:", outPath)


if __name__ == "__main__":
    main()
