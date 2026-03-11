#!/usr/bin/env python3
import argparse
import hashlib
import sys
from pathlib import Path

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
        print(f"ERROR hashing {filePath}: {exc}", file=sys.stderr)
        return None

def walkFiles(rootPath):
    for path in rootPath.rglob('*'):
        if path.is_file():
            yield path

def main():

    """
      python compare-two-dirs.py   C:\\users\\pbu\\Downloads\\riveda-mmd   C:\\users\\pbu\\Downloads\\riveda-mmd-02  

      when sure, add --delete 
    """

    parser = argparse.ArgumentParser( 
        description="Remove files from dirDupes that are already present in dir_main.")
    parser.add_argument("dir_dupes", type=str, help="directory containing redundant files")
    parser.add_argument("dir_main",  type=str)
    parser.add_argument("--delete", action="store_true", help="default is dry-run. If --delete is passed, this is True. Otherwise False")
    args = parser.parse_args()

    # Flip the logic for your code:
    dryRun = not args.delete
    if dryRun:
        print("Running in DRY RUN mode...")

    dirMain = Path(args.dir_main).expanduser().resolve()
    dirDupe = Path(args.dir_dupes).expanduser().resolve()

    if not dirDupe.exists() or not dirDupe.is_dir():
        print(f"ERROR: path does: {dirDupe}", file=sys.stderr)
        sys.exit(1)
        
    if not dirMain.exists() or not dirMain.is_dir():
        print(f"ERROR: path does: {dirDupe}", file=sys.stderr)
        sys.exit(1)

    if dirDupe == dirMain:
        print("ERROR: cannot be the exact same directory.", file=sys.stderr)
        sys.exit(1)


    print(f"{'dir1 (dupes)' :24} - {str(dirDupe)}")
    print(f"{'dir2 (main)'  :24} - {str(dirMain)}")

    if dryRun:
        print(f"{'mode':24} - DRY RUN (No files will be deleted)")
    print("")

    print("Scanning dirMain and compute hashes...")
    hashesMain = set()
    countsMain = 0
    for pth in walkFiles(dirMain):
        hsh = computeMd5(pth)
        if hsh is not None:
            hashesMain.add(hsh)
            countsMain += 1
            
    print(f" {countsMain:3} files ({len(hashesMain)} unique hashes) in dirMain.")
    print("")


    print("Scanning dirDupes for duplicates...")
    countDel = 0
    countKpt = 0  # count kept
    countErr = 0

    for pth in walkFiles(dirDupe):

        hsh = computeMd5(pth)
        
        if hsh is None:
            countErr += 1
            continue

        if hsh in hashesMain:
            if dryRun:
                print(f"\twould del {pth}")
                countDel += 1
            else:
                try:
                    pth.unlink()
                    print(f"\tdel {pth}")
                    countDel += 1
                except Exception as exc:
                    print(f"ERROR deleting {pth}: {exc}", file=sys.stderr)
                    countErr += 1
        else:
            countKpt += 1


    print("")
    print(f"{'--- SUMMARY ---':24}")
    if dryRun:
        print(f"{'to be deleted'  :28} - {countDel:4}")
    else:
        print(f"{'Files deleted'  :28} - {countDel:4}")
    print(f"{'Files kept (unique)':28} - {countKpt:4}")
    print(f"{'Errors'             :28} - {countErr:4}")

if __name__ == "__main__":
    main()