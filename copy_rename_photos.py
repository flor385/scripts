#! /usr/bin/env python3

"""
A Python script for copying photos from Lasta's SD card
to her internal/external drives, along with some folder
organization based on dates and names (that the user inputs
during runtime).
"""

import logging
import argparse
import os
import sys
from itertools import repeat
import datetime
from collections import defaultdict
import math
import getpass
import shutil


log = logging.getLogger(__name__)

DEFAULT_SRCS = [
    "E:\\DCIM\\"
    "/media/%s/6334-3266/DCIM/" % getpass.getuser(),
]

DEFAULT_DSTS = [
    "M:\\arhiva\\nikon",
    "D:\\",
    "/media/%s/KUTIJA/arhiva/nikon/" % getpass.getuser()
]


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default=None,
                        help="Folder in which files are sought")
    parser.add_argument("--dst", default=None,
                        help="Folder to which files are stored")
    parser.add_argument("--logging", required=False, default=logging.INFO,
                        help="Logging level")
    parser.add_argument("--datefmt", required=False, default="%Y%m%d",
                        help="Date format string")

    return parser.parse_args()

args = parse_args()


def src():
    if args.src is not None:
        return args.src

    for src in DEFAULT_SRCS:
        if os.path.isdir(src) and os.path.exists(src):
            return src

    log.error("ERROR: failed to detect a valid source, exiting.")
    sys.exit(1)


def dst():
    if args.dst is not None:
        return args.dst

    for dst in DEFAULT_DSTS:
        if os.path.isdir(dst):
            return dst

    log.error("ERROR: failed to detect a valid destination, exiting.")
    sys.exit(1)


def process():

    #   we need to accumulate file paths according to their datestrings
    files_per_date = defaultdict(list)

    log.info("Processing folder: %s", src())
    for folder, subfolders, files in os.walk(src()):

        #   filter out hidden files
        files = list(filter(lambda f: f[0] != '.', files))

        #   get full file paths
        file_paths = [os.path.join(folder, file) for file in files]

        #   get modification timestamps and convert them to date_strings
        mod_dates = list(map(
            datetime.datetime.strftime,
            map(datetime.datetime.fromtimestamp,
                map(os.path.getmtime, file_paths)),
            repeat(args.datefmt)))

        #   some debugging
        list(map(log.debug, repeat("%s - %s"), mod_dates, file_paths))

        for file_path, mod_date in zip(file_paths, mod_dates):
            files_per_date[mod_date].append(file_path)

    #   for each mod date ask for name
    for mod_date, file_paths in sorted(files_per_date.items()):
        name = input("Provide name for %d files with date %s: " % (
            len(file_paths), mod_date))

        #   see how much zero padding we need
        digits_fmt = "%%0%dd" % math.ceil(math.log10(len(file_paths) + 1))

        for ind, file_path in enumerate(file_paths):
            ext = os.path.splitext(file_path)[1]
            dst_path = os.path.join(
                dst(), "%s_%s_%s" % (mod_date, name, ext[1:].lower()),
                "%s_%s_%s%s" % (mod_date, digits_fmt % (ind + 1), name, ext))
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            log.debug("Copying %s -> %s", file_path, dst_path)
            shutil.copyfile(file_path, dst_path)


def main():
    logging.basicConfig(
        level=args.logging, format="  %(message)s")
    log.info("*** File copy-rename script for Lasta from Flo <3 ***")
    process()
    input("All done, press <Enter> key to exit...")


if __name__ == '__main__':
    main()
