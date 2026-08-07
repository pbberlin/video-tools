from pathlib import Path
import shutil
from PIL import Image

# Define target extensions (JPG/JPEG)
extensions = {".jpg", ".jpeg"}

# Setup backup directory path
dirBack = Path("before-width-reduction").resolve()
dirBack.mkdir(parents=True, exist_ok=True)

wdth = 800
wdth = 1024

for inPth in Path(".").rglob("*"):

    if not inPth.is_file():
        continue

    # Exclude files inside the backup directory
    if dirBack in inPth.resolve().parents:
        continue

    if inPth.suffix.lower() not in extensions:
        continue

    print(f"Processing: {inPth}")

    try:

        # original file to backup
        pthRel = inPth.relative_to(Path("."))
        pthBackup = dirBack / pthRel
        pthBackup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(inPth, pthBackup)
        print(f"\t backed up to: {pthBackup}")

        with Image.open(pthBackup) as img:
            # Handle color mode / alpha channels for JPEG
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.getchannel("A"))
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # new height maintaining aspect ratio
            width, height = img.size
            if width != wdth:
                new_height = max(1, int(round(height * (wdth / width))))
                resample_filter = getattr(Image, "Resampling", Image).LANCZOS
                img = img.resize((wdth, new_height), resample_filter)

            img.save(
                inPth,
                "JPEG",
                quality=90,
                optimize=True,
                progressive=True,
            )

        # metadata and timestamp from the backup to the new file
        shutil.copystat(pthBackup, inPth)
        print(f"Saved wdthpx version to: {inPth}\n")

    except Exception as exception:
        print(f"ERROR processing {inPth}: {exception}\n")