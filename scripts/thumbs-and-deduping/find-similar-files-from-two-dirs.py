#!/usr/bin/env python3
import argparse
import hashlib
import sys
from pathlib import Path

# Try to import image libraries for perceptual hashing
try:
    from PIL import Image
    import imagehash
    IMAGE_HASHING_AVAILABLE = True
except ImportError:
    IMAGE_HASHING_AVAILABLE = False
    print("WARNING: 'Pillow' or 'ImageHash' not installed. Similar image detection is disabled.", file=sys.stderr)
    print("To enable, run: pip install Pillow ImageHash\n", file=sys.stderr)


# Using set([]) to prevent the website from deleting the contents
IMAGE_EXTENSIONS = set(['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'])

def isImg(path):
    return path.suffix.lower() in IMAGE_EXTENSIONS


def computeMd5(filePath, chunkSize=1024 * 1024):
    hasher = hashlib.md5()
    try:
        with filePath.open('rb') as fh:
            while True:
                chunk = fh.read(chunkSize)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as exc:
        print("ERROR hashing %s: %s" % (filePath, exc), file=sys.stderr)
        return None


def imgInf(filePath):
    # Returns: phash, resolution (width * height), file_size_in_bytes
    if not IMAGE_HASHING_AVAILABLE:
        return None, 0, 0
    try:
        with Image.open(filePath) as img:
            phash = imagehash.phash(img)
            res = img.size[0] * img.size[1]
        sizeBytes = filePath.stat().st_size
        return phash, res, sizeBytes
    except Exception as exc:
        return None, 0, 0


def walkFiles(rootPath):
    for path in rootPath.rglob('*'):
        if path.is_file():
            yield path


def delFile(pth: Path, reason, dryRun):
    if dryRun:
        # print("\twould del %s/%s/%s" % (  pth.parent.parent.name , pth.parent.name ,  pth.name))
        print("\twould del %s/%s" % (  pth.parent.name ,  pth.name))
        print("\t\t %s" % (  reason))
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
        description="Remove redundant files, keeping only the highest quality images.")
    parser.add_argument("dir_dupes", type=str, help="directory containing redundant files")
    parser.add_argument("dir_main",  type=str)
    parser.add_argument("--delete", action="store_true", help="default is dry-run. If --delete is passed, this is True. Otherwise False")
    parser.add_argument("--sim-tolerance", type=int, default=2, help="Tolerance for similar images (0=exact visual match, 2=allows minor resizing artifacts, default: 2)")
    args = parser.parse_args()

    dryRun = not args.delete
    if dryRun:
        print("Running in DRY RUN mode...")

    dirMain = Path(args.dir_main).expanduser().resolve()
    dirDupe = Path(args.dir_dupes).expanduser().resolve()

    if not dirDupe.exists() or not dirDupe.is_dir():
        print("ERROR: path does not exist: %s" % dirDupe, file=sys.stderr)
        sys.exit(1)
        
    if not dirMain.exists() or not dirMain.is_dir():
        print("ERROR: path does not exist: %s" % dirMain, file=sys.stderr)
        sys.exit(1)

    if dirDupe == dirMain:
        print("ERROR: cannot be the exact same directory.", file=sys.stderr)
        sys.exit(1)


    print("%-24s - %s" % ("dir2 (main) ", dirMain))
    print("%-24s - %s" % ("dir1 (dupes)", dirDupe))

    if dryRun:
        print("%-24s - DRY RUN (No files will be deleted)" % "mode")
    print("")


    print("PASS 1: Scanning dirMain - computing MD5 and pHash")
    hashesMain = set([])
    pHashesMain = []  # store lists of: [phash, path, resolution, sizeBytes]
    countsMain = 0
    for pth in walkFiles(dirMain):
        hsh = computeMd5(pth)
        if hsh is not None:
            hashesMain.add(hsh)
            
        if isImg(pth):
            phsh, res, sz = imgInf(pth)
            if phsh is not None:
                pHashesMain.append([phsh, pth, res, sz])
                
        countsMain += 1            
    print(" %3d files (%d unique MD5s, %d Image Hashes) in dirMain." % (countsMain, len(hashesMain), len(pHashesMain)))
    print("")



    print("PASS 2: Scanning dirDupes for duplicates...")
    countDelExact = 0
    countDelSimDupe = 0
    countDelSimMain = 0
    countKpt = 0
    countErr = 0

    for pth in walkFiles(dirDupe):
        hsh = computeMd5(pth)
        if hsh is None:
            countErr += 1
            continue

        # exact dupes
        if hsh in hashesMain:
            if delFile(pth, "Exact MD5 Match", dryRun):
                countDelExact += 1
            else:
                countErr += 1
            continue


        # visual similarity (pHash)
        matched = False
        if isImg(pth):
            phsh, res, sz = imgInf(pth)
            if phsh is not None:
                for i in range(len(pHashesMain)):
                    main_phs = pHashesMain[i][0] # p Hash
                    main_pth = pHashesMain[i][1]
                    main_res = pHashesMain[i][2]
                    main_sze = pHashesMain[i][3]

                    if phsh - main_phs <= args.sim_tolerance:
                        matched = True
                        
                        # which is smaller/worse
                        dupeSmaller = False
                        
                        if res <= main_res:
                            dupeSmaller = True
                            reason = "dupe resolution eq or smaller (%d vs %d px)" % (res, main_res)
                        else:
                            dupeSmaller = False
                            reason = "dupe resolution larger (%d vs %d px)" % (main_res, res)


                        # deletion based on which is smaller
                        if dupeSmaller:
                            if delFile(pth, reason, dryRun):
                                countDelSimDupe += 1
                            else:
                                countErr += 1
                        else:
                            # main is WORSE! Delete main file.
                            if delFile(main_pth, reason, dryRun):
                                countDelSimMain += 1
                            else:
                                countErr += 1
                            
                            # Replace the entry in memory so we don't compare against the deleted file again!
                            # This allows the better file to become the new "King of the Hill"
                            pHashesMain[i] = [phsh, pth, res, sz]
                            
                        break # Stop checking other main hashes, move to next dupe file
        
        if not matched:
            countKpt += 1

    # --- SUMMARY ---
    print("")
    print("%-32s" % "--- SUMMARY ---")
    total_del = countDelExact + countDelSimDupe + countDelSimMain
    msg = 'Total to be deleted' if dryRun else 'Total files deleted'
    
    print("%-32s - %4d" % (msg, total_del))
    print("  %-30s - %4d" % ("exact dupes from dir_dupes", countDelExact))
    print("  %-30s - %4d" % ("smaller / equal from dir_dupes", countDelSimDupe))
    print("  %-30s - %4d" % ("smaller from dir_main)", countDelSimMain))
    print("%-32s - %4d" % ("Files kept (unique)", countKpt))
    print("%-32s - %4d" % ("Errors", countErr))

if __name__ == "__main__":

    """
      python compare-two-dirs.py   C:\\users\\pbu\\Downloads\\riveda-mmd   C:\\users\\pbu\\Downloads\\riveda-mmd-02  

      when sure, add --delete 
    """

    main()
