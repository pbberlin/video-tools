#!/usr/bin/env python3
import argparse
import sys
import os

from pathlib import Path

print("run: pip install Pillow ImageHash")
from PIL import Image, ImageFile
import imagehash


IMAGE_EXTENSIONS = set(['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'])

def isImg(path):
    return path.suffix.lower() in IMAGE_EXTENSIONS

def imgInf(filePath):
    # Returns: phash, resolution (width * height), file size
    try:
        with Image.open(filePath) as img:
            phsh = imagehash.phash(img)
            # print(f"\tphsh is {phsh} of type {type(phsh)} ")
            res  = img.width * img.height
            # print(f"\tres is  {img.width} * {img.height} = {res} ")
            sze  = filePath.stat().st_size
            # print(f"\tfile size  is {sze/1024/1024:4.3f} MB ")
            return phsh, res, sze
    except Exception as exc:
        print("ERROR processing image %s: %s" % (filePath, exc), file=sys.stderr)
        os._exit(-1)
        return None, 0, 0


def walkFiles(rootPath):
    for path in rootPath.rglob('*'):
        if ".thumbs" in path.parts:
            continue
        if path.is_file():
            yield path



def delFile(pth: Path, reason, dryRun):
    if dryRun:
        print("\twould del %s/%s" % ( pth.parent.name , pth.name))
        print("\t\t %s" % ( reason))
        return True
    else:
        try:
            pth.unlink()
            print("\tdel %s [%s]" % (pth, reason))
            return True
        except Exception as exc:
            print("ERROR deleting %s: %s" % (pth, exc), file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
    description="Remove redundant files, keeping only highest quality images.")
    parser.add_argument("dir_target", type=str, help="directory containing images to scan")
    parser.add_argument("--delete",  action="store_true", help="default is dry-run. If --delete is passed, this is True. Otherwise False")
    parser.add_argument("--sim-tolerance", type=int, default=2, help="Tolerance for similar images (0=exact visual match, 2=allows minor resizing artifacts, default: 2)")
    args = parser.parse_args()

    dryRun = not args.delete
    if dryRun:
        print("Running in DRY RUN mode...")

    dirTarget = Path(args.dir_target).expanduser().resolve()

    if not dirTarget.exists() or not dirTarget.is_dir():
        print("ERROR: path does not exist: %s" % dirTarget, file=sys.stderr)
        sys.exit(1)

    print("%-24s - %s" % ("dirTarget ", dirTarget))

    if dryRun:
        print("%-24s - DRY RUN (No files will be deleted)" % "mode")
    print("")


    print("Scanning dirTarget for similar images...")
    seenImages = []  # store lists of: [phash, path, resolution, sizeBytes]
    countDelSimNew = 0
    countDelSimOld = 0
    countKpt = 0
    countErr = 0

    for pth in walkFiles(dirTarget):
        if not isImg(pth):
            continue

        phsh, res, sz = imgInf(pth)
        if phsh is None:
            countErr += 1
            continue

        # visual similarity (pHash)
        matched = False
        for idx1, seenImg in enumerate(seenImages):

            seenPhs = seenImg[0] # p Hash
            seenPth = seenImg[1]
            seenRes = seenImg[2]
            seenSze = seenImg[3]

            if phsh - seenPhs <= args.sim_tolerance:
                matched = True

                # which is smaller/worse
                newIsSmaller = False

                if res <= seenRes:
                    newIsSmaller = True
                    reason = "new image resolution eq or smaller (%d vs %d px)" % (res, seenRes)
                else:
                    newIsSmaller = False
                    reason = "old image resolution eq or smaller (%d vs %d px)" % (seenRes, res)


                # deletion based on which is smaller
                if newIsSmaller:
                    if delFile(pth, reason, dryRun):
                        countDelSimNew += 1
                    else:
                        countErr += 1
                else:
                    # old is WORSE! Delete old file.
                    if delFile(seenPth, reason, dryRun):
                        countDelSimOld += 1
                    else:
                        countErr += 1

                    # replace entry - so we don't compare against the deleted file again!
                    #   => better file becomes new "King"
                    seenImages[idx1] = [phsh, pth, res, sz]

                break # Stop checking other seen hashes, move to next file

        if not matched:
            seenImages.append([phsh, pth, res, sz])
            countKpt += 1


    # --- SUMMARY ---
    print("")
    print("%-32s" % "--- SUMMARY ---")
    totalDel = countDelSimNew + countDelSimOld
    msg = 'Total to be deleted' if dryRun else 'Total files deleted'

    print("%-32s - %4d" % (msg, totalDel))
    print("    %-28s - %4d" % ("new images deleted (smaller)", countDelSimNew))
    print("    %-28s - %4d" % ("old images deleted (smaller)", countDelSimOld))
    print("%-32s - %4d" % ("Files kept (unique)", countKpt))
    print("%-32s - %4d" % ("Errors", countErr))



if __name__ == "__main__":
    """
    python find-similar-images.py   C:\\users\\pbu\\Downloads\\riveda-mmd

    when sure, add --delete

    --sim-tolerance=17
    """

    main()