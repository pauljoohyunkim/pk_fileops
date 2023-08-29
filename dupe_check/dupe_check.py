#!/bin/python
# Debug with python -m dupe_check.dupe_check
import os
from sys import argv, exit
from hasher.hasher import sha256_hexdigest
from tqdm import tqdm

def main():
    argc = len(argv)

    if argc == 1:
        print(f"Usage: {argv[0]} [Path] ...")
        exit(1)
    
    # Removing duplicates from the given paths
    dirlist = list(set(argv[1:]))

    # Walk and get a list of files
    print("Walking through the directories...")
    file_digest_pair_list = []
    for dirname in dirlist:
        for root, dirs, files in tqdm(os.walk(dirname)):
            for file in files:
                filename = os.path.join(root, file)
                sha256digest = sha256_hexdigest(filename)
                # Check if there was error.
                if not sha256digest:
                    continue
                file_digest_pair_list.append((filename, sha256digest))

    print("Processing the file hash list.")
    # Process the list such that it creates a dictionary of the form hexdigest:[file path]
    hash_to_filename = dict()
    for filename, hexdigest in tqdm(file_digest_pair_list):
        if hexdigest in hash_to_filename.keys():
            hash_to_filename[hexdigest].append(filename)
        else:
            hash_to_filename[hexdigest] = [filename]
    
    # Show the entries that are duplicates only.
    for key, value in tqdm(hash_to_filename.items()):
        if len(value) == 1:
            continue
        print(value) 


if __name__ == "__main__":
    main()