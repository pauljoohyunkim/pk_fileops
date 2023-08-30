#!/bin/python
# Debug with python -m sim_image.sim_image
from PIL import Image
from imagehash import average_hash
import os
from argparse import ArgumentParser
from sys import argv, exit
from tqdm import tqdm
from gc import collect
from itertools import combinations
from sim_image.image_file import image_with_pil

def main():
    try:
        argc = len(argv)
        # Argument parsing
        parser = ArgumentParser(description="Checks for duplicate files by comparing hashes")
        parser.add_argument("directory", nargs="*")
        parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
        parser.add_argument("-a", "--absolute", help="Output as absolute paths", action="store_true")
        parser.add_argument("-p", "--pairwise", help="Print out a list of \"pairwise similar\" images", action="store_true")
        parser.add_argument("-o", "--output", help="Output the result to the specified file.", nargs=1)
        parser.add_argument("-t", "--threshold", help="Threshold as to what constitutes as \"similar\" (min: 0, max: 64, default: 5)", nargs=1, type=int)
        args = parser.parse_args()

        threshold=5
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
                print("Absolute paths enabled.")

        pairwise = False
        if args.pairwise:
            pairwise = True
            if verbose:
                print("Outputting pairwise similar images.")
        
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
        # Process the list such that pairwise similar images are in a list of the form
        # [((Image1Path, Image1Hash), (Image2Path, Image2Hash))]
        similar_pairs = []
        for tuple1, tuple2 in progresser(combinations(file_digest_pair_list, 2)):
            if tuple1[1] - tuple2[1] <= threshold:
                similar_pairs.append((tuple1[0], tuple2[0]))
        
        del file_digest_pair_list
        collect()

        if pairwise:
            for pair in similar_pairs:
                print(f"{pair[0]};{pair[1]}")
            exit(0)
        
        # For default, non-pairwise option, partitioning to "similar images"
        # Type: [{Image}]
        if verbose:
            print("Linking pairwise list into partitions")
        partition_of_images = []
        for pair in progresser(similar_pairs):
            added = False
            for partition in partition_of_images:
                if pair[0] in partition or pair[1] in partition:
                    partition.add(pair[0])
                    partition.add(pair[1])
                    added = True
                    break
            if added:
                continue
            partition_of_images.append({pair[0],pair[1]})
        
        for partition in partition_of_images:
            line = ';'.join(partition)
            print(line)
        
    except KeyboardInterrupt:
        exit(2)


if __name__ == "__main__":
    main()
