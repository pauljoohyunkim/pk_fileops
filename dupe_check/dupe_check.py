import os
from sys import argv, exit
from hasher.hasher import sha256_hexdigest

def main():
    argc = len(argv)
    if argc == 1:
        print("Usage: {argv[1]} [Path] ...")
        exit(1)