#!/usr/bin/env python3
"""
Grabs the latest version of every libretro core from the build bot.
"""

__author__ = "Melon Bread"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os
import zipfile
from shutil import rmtree
from urllib.request import urlretrieve

URL = 'https://buildbot.libretro.com/nightly'

PLATFORM = 'linux/x86_64'

CORE_LOCATION = '~/.config/retroarch/cores/'


def main(args):
    """ Where the magic happens """
    download_cores()
    extract_cores()
    if not args.keep:
        clean_up()


def download_cores():
    """ Downloads every core to the working directory """

    cores = []

    # Makes core directory to store archives if needed
    if not os.path.isdir('cores'):
        os.makedirs("cores")

    # Downloads a list of all the cores available
    urlretrieve('{}/{}/latest/.index-extended'.format(URL, PLATFORM),
                'cores/index')
    print('Obtained core index!')

    # Adds all the core's file names to a list
    core_index = open('cores/index')

    for line in core_index:
        file_name = line.split(' ', 2)[2:]
        cores.append(file_name[0].rstrip())
    core_index.close()
    cores.sort()

    # Downloads each core from the list
    for core in cores:
        urlretrieve('{}/{}/latest/{}'.format(URL, PLATFORM, core),
                    'cores/{}'.format(core))
        print('Downloaded {} ...'.format(core))

    # Removes index file for easier extraction
    os.remove('cores/index')


def extract_cores():
    """ Extracts each downloaded core to the RA core directory """
    print('Extracting all cores to: {}'.format(CORE_LOCATION))

    for file in os.listdir('cores'):
        archive = zipfile.ZipFile('cores/{}'.format(file))
        archive.extractall(CORE_LOCATION)
        print('Extracted {} ...'.format(file))
    pass


def clean_up():
    """ Removes all the downloaded files """
    rmtree('cores/')
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--keep', action='store_true',
                    help='Keeps downloaded core archives')

    args = parser.parse_args()
    main(args)
    pass
