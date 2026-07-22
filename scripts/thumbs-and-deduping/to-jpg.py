# jpeg, webp, png - to jpg

from pathlib import Path

from PIL import Image
import shutil


extensions = {
    ".jpeg",
    ".png",
    ".webp",
}


for idx1, inputPath in enumerate(Path(".").rglob("*")):
    if inputPath.suffix.lower() not in extensions:
        continue

    outputPath = inputPath.with_suffix(".jpg")

    print(f"Converting: {inputPath}")

    try:
        with Image.open(inputPath) as image:
            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.getchannel("A"))
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")

            image.save(
                outputPath,
                "JPEG",
                # quality=95,
                quality=90,
                optimize=True,
                progressive=True,
            )

        shutil.copystat(inputPath, outputPath)
        
        inputPath.unlink()
        print(f"Removed:    {inputPath}")

    except Exception as exception:
        print(f"ERROR: {inputPath}")
        print(exception)