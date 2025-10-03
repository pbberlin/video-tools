#!/usr/bin/env python3
import argparse
import hashlib
import itertools
import os
import sys
from pathlib import Path
from datetime import datetime

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

def gatherFileMetadata(rootPath):
    fileInfoList = []
    for path in walkFiles(rootPath):
        fileHash = computeMd5(path)
        if fileHash is None:
            # Error already printed; skip this file
            continue  # explicit skip is fine; we did not swallow the exception
        try:
            stat = path.stat()
            sizeBytes = stat.st_size
            mtime = stat.st_mtime
        except Exception as exc:
            print(f"ERROR stat {path}: {exc}", file=sys.stderr)
            continue
        record = {
            "path": path,
            "dir": path.parent,
            "name": path.name,
            "hash": fileHash,
            "size": sizeBytes,
            "mtime": mtime,
        }
        fileInfoList.append(record)
    return fileInfoList

def buildIndexes(fileInfoList):
    hashToFiles = {}
    dirToHashes = {}
    dirToFiles = {}
    dirHashToFiles = {}

    for rec in fileInfoList:
        fileHash = rec["hash"]
        dirPath = rec["dir"]

        if fileHash not in hashToFiles:
            hashToFiles[fileHash] = []
        hashToFiles[fileHash].append(rec)

        if dirPath not in dirToHashes:
            dirToHashes[dirPath] = set()
        dirToHashes[dirPath].add(fileHash)

        if dirPath not in dirToFiles:
            dirToFiles[dirPath] = []
        dirToFiles[dirPath].append(rec)

        key = (dirPath, fileHash)
        if key not in dirHashToFiles:
            dirHashToFiles[key] = []
        dirHashToFiles[key].append(rec)

    return hashToFiles, dirToHashes, dirToFiles, dirHashToFiles

def candidateDirectoryPairs(hashToFiles):
    # Build set of directory pairs that share at least one hash
    pairSet = set()
    for fileHash, recs in hashToFiles.items():
        dirs = []
        for rec in recs:
            dirPath = rec["dir"]
            dirs.append(dirPath)
        # unique directories for this hash
        uniqueDirs = []
        seen = set()
        for d in dirs:
            if d not in seen:
                uniqueDirs.append(d)
                seen.add(d)
        # all unordered pairs of directories for this hash
        for i in range(len(uniqueDirs)):
            for j in range(i + 1, len(uniqueDirs)):
                d1 = uniqueDirs[i]
                d2 = uniqueDirs[j]
                # store as ordered tuple to make set stable
                if str(d1) <= str(d2):
                    pairSet.add((d1, d2))
                else:
                    pairSet.add((d2, d1))
    return pairSet

def newestSharedMtimeForPair(leftDir, rightDir, sharedHashes, dirHashToFiles):
    newest = None
    for h in sharedHashes:
        keyLeft = (leftDir, h)
        keyRight = (rightDir, h)
        # Left files with this hash
        if keyLeft in dirHashToFiles:
            leftList = dirHashToFiles[keyLeft]
            for rec in leftList:
                t = rec["mtime"]
                if newest is None or t > newest:
                    newest = t
        # Right files with this hash
        if keyRight in dirHashToFiles:
            rightList = dirHashToFiles[keyRight]
            for rec in rightList:
                t = rec["mtime"]
                if newest is None or t > newest:
                    newest = t
    if newest is None:
        return None
    return newest

def topNewerFilesSince(dirPath, thresholdMtime, dirToFiles, limit=20):
    newer = []
    if dirPath in dirToFiles:
        files = dirToFiles[dirPath]
        for rec in files:
            if rec["mtime"] > thresholdMtime:
                delta = rec["mtime"] - thresholdMtime
                newer.append((rec, delta))
    # sort by delta descending, then by name for stability
    newerSorted = sorted(newer, key=lambda x: (-x[1], x[0]["name"]))
    result = []
    count = 0
    for item in newerSorted:
        result.append(item)
        count += 1
        if count >= limit:
            break
    return result

def formatSeconds(seconds):
    # Show as days/hours/minutes/seconds compactly
    remaining = int(seconds)
    days = remaining // 86400
    remaining = remaining % 86400
    hours = remaining // 3600
    remaining = remaining % 3600
    minutes = remaining // 60
    secondsLeft = remaining % 60
    parts = []
    if days != 0:
        parts.append(f"{days}d")
    if hours != 0:
        parts.append(f"{hours}h")
    if minutes != 0:
        parts.append(f"{minutes}m")
    if secondsLeft != 0 or len(parts) == 0:
        parts.append(f"{secondsLeft}s")
    text = ""
    for i in range(len(parts)):
        if i == 0:
            text = parts[i]
        else:
            text = f"{text} {parts[i]}"
    return text

def printDirectoryPairReport(leftDir, rightDir, dirToHashes, dirToFiles, dirHashToFiles):
    leftHashes = set()
    rightHashes = set()

    if leftDir in dirToHashes:
        for h in dirToHashes[leftDir]:
            leftHashes.add(h)
    if rightDir in dirToHashes:
        for h in dirToHashes[rightDir]:
            rightHashes.add(h)

    shared = set()
    for h in leftHashes:
        if h in rightHashes:
            shared.add(h)

    if len(shared) == 0:
        return  # nothing to report

    leftOnly = set()
    for h in leftHashes:
        if h not in shared:
            leftOnly.add(h)

    rightOnly = set()
    for h in rightHashes:
        if h not in shared:
            rightOnly.add(h)

    # Header for the pair
    leftStr = str(leftDir)
    rightStr = str(rightDir)
    print(f"{leftStr:24} - {rightStr:24}")

    # Shared/exclusive counts
    print(f"{'shared':24} - {len(shared):24}")
    print(f"{'exclusive left':24} - {len(leftOnly):24}")
    print(f"{'exclusive right':24} - {len(rightOnly):24}")

    # Newest shared file mtime (across both dirs)
    newestShared = newestSharedMtimeForPair(leftDir, rightDir, shared, dirHashToFiles)
    if newestShared is None:
        print(f"{'newest shared mtime':24} - {'(none)':24}")
        return
    newestSharedDt = datetime.fromtimestamp(newestShared)
    print(f"{'newest shared mtime':24} - {newestSharedDt.isoformat():24}")

    # Top newer files on left
    leftNewer = topNewerFilesSince(leftDir, newestShared, dirToFiles, limit=20)
    print(f"{'NEWER on left (top 20)':24} - {'Δ since newest shared':24}")
    if len(leftNewer) == 0:
        print(f"{'(none)':24} - {'':24}")
    else:
        for rec, delta in leftNewer:
            deltaText = formatSeconds(delta)
            itemLeft = str(rec['path'])
            print(f"{itemLeft:24} - {deltaText:24}")

    # Top newer files on right
    rightNewer = topNewerFilesSince(rightDir, newestShared, dirToFiles, limit=20)
    print(f"{'NEWER on right (top 20)':24} - {'Δ since newest shared':24}")
    if len(rightNewer) == 0:
        print(f"{'(none)':24} - {'':24}")
    else:
        for rec, delta in rightNewer:
            deltaText = formatSeconds(delta)
            itemRight = str(rec['path'])
            print(f"{itemRight:24} - {deltaText:24}")

    print("")  # spacer line

def main():
    parser = argparse.ArgumentParser(description="Traverse a directory subtree, MD5 every file, and report directory pairs that share duplicate files.")
    parser.add_argument("root", type=str, help="Root directory to traverse")
    parser.add_argument("--min-shared", type=int, default=1, help="Only report directory pairs with at least this many shared files (default: 1)")
    args = parser.parse_args()

    rootPath = Path(args.root).expanduser().resolve()

    if not rootPath.exists():
        print(f"ERROR: root path does not exist: {rootPath}", file=sys.stderr)
        sys.exit(1)
    if not rootPath.is_dir():
        print(f"ERROR: root path is not a directory: {rootPath}", file=sys.stderr)
        sys.exit(1)

    print(f"{'root':24} - {str(rootPath):24}")
    print("")

    fileInfoList = gatherFileMetadata(rootPath)
    print(f"{'files hashed':24} - {len(fileInfoList):24}")

    hashToFiles, dirToHashes, dirToFiles, dirHashToFiles = buildIndexes(fileInfoList)

    # Directory stats of duplicate files (per directory)
    print("")
    print(f"{'directory':24} - {'duplicate file count':24}")
    for dirPath, hashes in dirToHashes.items():
        dupCount = 0
        for h in hashes:
            files = hashToFiles.get(h, [])
            if len(files) > 1:
                dupCount += 1
        print(f"{str(dirPath):24} - {dupCount:24}")

    print("")
    print(f"{'DIRECTORY PAIRS WITH SHARED FILES':24} - {'':24}")
    pairs = candidateDirectoryPairs(hashToFiles)

    # Filter by min-shared
    filteredPairs = []
    for leftDir, rightDir in pairs:
        leftHashes = dirToHashes.get(leftDir, set())
        rightHashes = dirToHashes.get(rightDir, set())
        sharedCount = 0
        for h in leftHashes:
            if h in rightHashes:
                sharedCount += 1
        if sharedCount >= args.min_shared:
            filteredPairs.append((leftDir, rightDir))

    # Sort pairs for deterministic output
    filteredPairsSorted = sorted(filteredPairs, key=lambda p: (str(p[0]), str(p[1])))

    for leftDir, rightDir in filteredPairsSorted:
        printDirectoryPairReport(leftDir, rightDir, dirToHashes, dirToFiles, dirHashToFiles)

if __name__ == "__main__":
    main()


# python dupe_dirs.py /path/to/root
# Only show pairs with >= 3 shared files:
# python dupe-dirs.py "C:\users\pbu\dropbox\video\own-productions\__for-girls\for-sashka\2025-06-sashka-loyalfans--all-her-pics\" --min-shared 3
