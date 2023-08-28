#!/bin/python
# Debug with python -m dupe_check.dupe_check
import os
from sys import argv, exit
from hasher.hasher import sha256_hexdigest

def main():
    argc = len(argv)

    if argc == 1:
        print(f"Usage: {argv[0]} [Path] ...")
        exit(1)
    
    # Removing duplicates from the given paths
    dirlists = list(set(argv[1:]))

if __name__ == "__main__":
    main()