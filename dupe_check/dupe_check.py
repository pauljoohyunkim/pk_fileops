#!/bin/python
# Debug with python -m dupe_check.dupe_check
import os
from argparse import ArgumentParser
from sys import argv, exit
from hasher.hasher import sha256_hexdigest
from tqdm import tqdm
from gc import collect

def main():
    argc = len(argv)
    # Argument parsing
    parser = ArgumentParser(description="Checks for duplicate files by comparing hashes")
    parser.add_argument("directory", nargs="*")
    parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
    args = parser.parse_args()

    verbose = False
    if args.verbose:
        verbose = True
        print("Verbose output enabled.")

    progresser = tqdm if verbose else lambda x : x

    if argc == 1 or args.directory == []:
        parser.print_usage()
        exit(1)
    
    dirlist = list(set(args.directory))

    # Walk and get a list of files
    if verbose:
        print("Walking through the directories...")
    file_digest_pair_list = []
    for dirname in dirlist:
        for root, dirs, files in progresser(os.walk(dirname)):
            for file in files:
                filename = os.path.join(root, file)
                sha256digest = sha256_hexdigest(filename)
                # Check if there was error.
                if not sha256digest:
                    continue
                file_digest_pair_list.append((filename, sha256digest))
    
    del dirlist
    collect()

    if verbose:
        print("Processing the file hash list.")
    # Process the list such that it creates a dictionary of the form hexdigest:[file path]
    hash_to_filename = dict()
    for filename, hexdigest in progresser(file_digest_pair_list):
        if hexdigest in hash_to_filename.keys():
            hash_to_filename[hexdigest].append(filename)
        else:
            hash_to_filename[hexdigest] = [filename]

    del file_digest_pair_list
    collect()
    
    # Show the entries that are duplicates only.
    for key, value in hash_to_filename.items():
        if len(value) == 1:
            continue
        print(value) 


if __name__ == "__main__":
    main()