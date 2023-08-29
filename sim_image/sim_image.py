#!/bin/python
# Debug with python -m sim_image.sim_image
from PIL import Image
from imagehash import average_hash
import os
from argparse import ArgumentParser
from sys import argv, exit
from tqdm import tqdm
from gc import collect
from sim_image.image_file import image_with_pil

def main():
    try:
        argc = len(argv)
        # Argument parsing
        parser = ArgumentParser(description="Checks for duplicate files by comparing hashes")
        parser.add_argument("directory", nargs="*")
        parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
        parser.add_argument("-a", "--absolute", help="Output as absolute paths", action="store_true")
        parser.add_argument("-o", "--output", help="Output the result to the specified file.", nargs=1)
        parser.add_argument("-t", "--threshold", help="Threshold as to what constitutes as \"similar\" (min: 0, max: 64)", nargs=1, type=int)
        args = parser.parse_args()

        threshold=32
        if args.threshold:
            threshold = args.threshold[0]

        verbose = False
        if args.verbose:
            verbose = True
            print("Verbose output enabled.")

        absolute = False
        if args.absolute:
            absolute = True
            if verbose:
                print("Absolute paths enabled")
        
        outputfile = None
        if args.output:
            outputfile = args.output[0]
            if verbose:
                print(f"Outputting the result to {outputfile}")

        progresser = tqdm if verbose else (lambda x : x)
        pather = (lambda x : os.path.abspath(x)) if absolute else (lambda x : x)

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
                    filename = pather(os.path.join(root, file))
                    image = image_with_pil(filename)
                    if not image:
                        continue
                    imagehash = average_hash(image)
                    # Check if there was error.
                    file_digest_pair_list.append((filename, imagehash))
        
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
        if outputfile:
            with open(outputfile, "a") as file:
                for key, value in hash_to_filename.items():
                    if len(value) == 1:
                        continue
                    line = ';'.join(value)
                    print(line)
                    file.write(line + "\n")
        else:
            for key, value in hash_to_filename.items():
                if len(value) == 1:
                    continue
                print(';'.join(value))
    except KeyboardInterrupt:
        exit(2)


if __name__ == "__main__":
    main()
