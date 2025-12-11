import subprocess
import shutil
import tempfile
from pathlib import Path

# ---- Settings (adjust as needed) ----
targetWidth  = 1920
targetHeight = 1080
secondsPerImage = 1.4
outputFile = "slideshow.mp4"
outputFps = 25  # final video fps
# -------------------------------------


def main():
    cwd = Path.cwd()

    jpgFiles = []
    for pattern in ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]:
        for p in sorted(cwd.glob(pattern)):
            jpgFiles.append(p)

    jpgFiles = sorted(jpgFiles, key=lambda x: x.name.lower())

    if len(jpgFiles) == 0:
        print("No JPG images found in the current directory.")
        return

    tempDir = None
    try:
        tempDir = Path(tempfile.mkdtemp(prefix="slideshow_tmp_"))

        index = 0
        for imgPath in jpgFiles:
            indexString = f"{index:06d}"
            destPath = tempDir / f"{indexString}.jpg"
            try:
                shutil.copy2(imgPath, destPath)
            except Exception as e:
                print(f"Failed to copy {imgPath} -> {destPath}: {e}")
            index += 1

        # Build the scaling + padding filter:
        # - scale down to fit within targetWidth x targetHeight (keep aspect)
        # - pad with black bars to exactly targetWidth x targetHeight
        # - ensure yuv420p for better compatibility
        vfFilter = (
            f"scale={targetWidth}:{targetHeight}:force_original_aspect_ratio=decrease,"
            f"pad={targetWidth}:{targetHeight}:(ow-iw)/2:(oh-ih)/2:black,"
            f"format=yuv420p"
        )

        # Read images at a rate so each image lasts secondsPerImage
        # e.g. framerate = 1 / 1.4 ≈ 0.7142857 images/sec
        inputFramerate = 1.0 / secondsPerImage

        # Use the numbered images in tempDir as the input sequence
        inputPattern = str((tempDir / "%06d.jpg").as_posix())

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", f"{inputFramerate}",
            "-i", inputPattern,
            "-vf", vfFilter,
            "-r", f"{outputFps}",
            "-movflags", "+faststart",
            "-pix_fmt", "yuv420p",
            outputFile,
        ]

        print("Running ffmpeg...")
        print(" ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg failed with exit code {e.returncode}")
            print(e)
            return

        print(f"Done. Wrote {outputFile}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if tempDir is not None and tempDir.exists():
            try:
                # Clean up the temporary directory
                for child in tempDir.iterdir():
                    try:
                        child.unlink()
                    except Exception as e:
                        print(f"Failed to delete {child}: {e}")
                try:
                    tempDir.rmdir()
                except Exception as e:
                    print(f"Failed to remove temp dir {tempDir}: {e}")
            except Exception as e:
                print(f"Cleanup error: {e}")

if __name__ == "__main__":
    main()
