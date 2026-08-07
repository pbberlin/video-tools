import json
from collections import defaultdict
from itertools import combinations
import os
import time

# ==============================================================================
# SETTINGS (Change these if needed)
# ==============================================================================
JSON_FILE = "dupes.json"
ALLOWED_EXTENSIONS = {".mp4", ".mkv"}  # Set to empty set () to allow all
MIN_SIZE_BYTES = 24 * 1024              # 24 KB (24,576 bytes)
# ==============================================================================


def analyze_directory_duplicates():
    if not os.path.exists(JSON_FILE):
        print(f"File '{JSON_FILE}' not found.")
        return

    start_time = time.time()
    print(f"Loading {JSON_FILE}...")

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    folder_groups = defaultdict(set)
    folder_files = defaultdict(list)
    folder_group_file_counts = defaultdict(lambda: defaultdict(int))

    total_filtered_files = 0

    for item_group in data:
        gid = item_group.get("GroupId")
        if not gid:
            continue

        for item in item_group.get("Items", []):
            # Size check
            size_long = item.get("SizeLong", 0)
            if size_long <= MIN_SIZE_BYTES:
                continue

            # Extension check
            path = item.get("Path", "")
            if ALLOWED_EXTENSIONS:
                ext = os.path.splitext(path)[1].lower()
                if ext not in ALLOWED_EXTENSIONS:
                    continue

            folder = item.get("Folder")
            if folder and path:
                folder_groups[folder].add(gid)
                folder_files[folder].append(path)
                folder_group_file_counts[folder][gid] += 1
                total_filtered_files += 1

    folders = list(folder_groups.keys())
    print(f"Indexed {total_filtered_files} matching files across {len(folders)} folders in {time.time() - start_time:.2f}s.")
    print("Comparing directories...\n")

    exact_matches = []
    subsets = []
    partial_overlaps = []

    for f1, f2 in combinations(folders, 2):
        g1, g2 = folder_groups[f1], folder_groups[f2]
        shared_clusters = g1 & g2

        if not shared_clusters:
            continue

        f1_matched_files = sum(folder_group_file_counts[f1][gid] for gid in shared_clusters)
        f2_matched_files = sum(folder_group_file_counts[f2][gid] for gid in shared_clusters)

        res = {
            "dir1": f1,
            "dir2": f2,
            "f1_matched_files": f1_matched_files,
            "f2_matched_files": f2_matched_files,
            "f1_total_files": len(folder_files[f1]),
            "f2_total_files": len(folder_files[f2]),
        }

        if g1 == g2:
            exact_matches.append(res)
        elif g1.issubset(g2):
            res["subset"] = f1
            res["superset"] = f2
            subsets.append(res)
        elif g2.issubset(g1):
            res["subset"] = f2
            res["superset"] = f1
            subsets.append(res)
        else:
            partial_overlaps.append(res)


    if True:
        print("=" * 80)
        print(f"1. EXACT MATCH DIRECTORIES ({len(exact_matches)} pairs)")
        print("   (Both folders contain identical duplicate files)")
        print("-" * 80)
        if not exact_matches:
            print("  None found.")
        for r in exact_matches:
            count_str = f" ({r['f1_matched_files']} matching files)" if r['f1_matched_files'] != 1 else ""
            print(f"• EXACT MATCH{count_str}:")
            print(f"  Dir A: {r['dir1']}")
            print(f"  Dir B: {r['dir2']}\n")


    if True:
        print(f"\n2. SUBSET DIRECTORIES ({len(subsets)} pairs)")
        print("   (All duplicate files in the subset folder exist inside the superset folder)")
        print("-" * 80)
        if not subsets:
            print("  None found.")
        for r in subsets:
            is_d1_sub = (r['subset'] == r['dir1'])
            sub_matched = r['f1_matched_files'] if is_d1_sub else r['f2_matched_files']
            spr_matched = r['f2_matched_files'] if is_d1_sub else r['f1_matched_files']
            super_total = r['f2_total_files']   if is_d1_sub else r['f1_total_files']
            extra_files = super_total - spr_matched

            count_str = f" ({sub_matched} matching files)" if sub_matched != 1 else ""
            # print(f"• SUBSET RELATIONSHIP{count_str}:")
            # print(f"• SUPERSET - SUBSET")
            outputP1 = f"{spr_matched:2} matching f(s) + {extra_files:2} extra dupe file(s)"
            print(f"  [SUPERSET] {outputP1:42} {r['superset']} ")
            outputP2 = f"{sub_matched:2} file{'s' if sub_matched != 1 else ''}"
            print(f"  [SUBSET]   {outputP2:42} {r['subset']  } ")
            print()


    if False:
        print(f"\n3. PARTIAL OVERLAP DIRECTORIES ({len(partial_overlaps)} pairs)")
        print("   (some matching files, each dir has distinct files)")
        print("-" * 80)
        if not partial_overlaps:
            print("  None found.")
        for r in partial_overlaps:
            print(f"• PARTIAL OVERLAP:")
            print(f"  Dir A:  {r['f1_matched_files']:2}/{r['f1_total_files']:2} files match Dir B   {r['dir1']} ")
            print(f"  Dir B:  {r['f2_matched_files']:2}/{r['f2_total_files']:2} files match Dir A   {r['dir2']} ")
            print()

    print(f"Completed in {time.time() - start_time:.2f} seconds.")


# --- Run ---
if __name__ == "__main__":
    analyze_directory_duplicates()