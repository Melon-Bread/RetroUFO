#!/usr/bin/env python3
"""
Grabs the latest version of every libretro core from the build bot.
"""

__author__ = "Melon Bread"
__version__ = "0.9.1"
__license__ = "MIT"

import argparse
import os
import platform
import sys
import zipfile
from shutil import rmtree
from urllib.request import urlretrieve

URL = 'https://buildbot.libretro.com/nightly'

# These are the default core locations with normal RetroArch installs based off of 'retroarch.default.cfg`
CORE_LOCATION = {
    'linux': '{}/.config/retroarch/cores'.format(os.path.expanduser('~')),
    'apple/osx': '/Applications/RetroArch.app/Contents/Resources/cores',  # macOS
    'windows': '{}/AppData/Roaming/RetroArch/cores'.format(os.path.expanduser('~'))
}


def main(_args):
    """ Where the magic happens """

    # If a platform and/or architecture is not supplied it is grabbed automatically
    target_platform = _args.platform if _args.platform else get_platform()
    architecture = _args.architecture if _args.architecture else get_architecture()
    location = _args.location if _args.location else CORE_LOCATION[target_platform]

    download_cores(target_platform, architecture)
    extract_cores(location)

    if not args.keep:
        clean_up()


def get_platform():
    """ Gets the Platform and Architecture if not supplied """

    if platform.system() == 'Linux':
        return 'linux'
    elif platform.system() == 'Darwin':  # macOS
        return 'apple/osx'
    elif platform.system() == 'Windows' or 'MSYS_NT' in platform.system():  # Checks for MSYS environment as well
        return 'windows'
    else:
        print('ERROR: Platform not found or supported')
        sys.exit(0)


def get_architecture():
    """ Gets the Platform and Architecture if not supplied """

    if '64' in platform.architecture()[0]:
        return 'x86_64'

    elif '32' in platform.architecture()[0]:
        return 'x86'
    else:
        print('ERROR: Architecture not found or supported')
        sys.exit(0)


def download_cores(_platform, _architecture):
    """ Downloads every core to the working directory """

    cores = []

    # Makes core directory to store archives if needed
    if not os.path.isdir('cores'):
        os.makedirs("cores")

    # Downloads a list of all the cores available
    urlretrieve('{}/{}/{}/latest/.index-extended'.format(URL, _platform, _architecture),
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
        urlretrieve('{}/{}/{}/latest/{}'.format(URL, _platform, _architecture, core),
                    'cores/{}'.format(core))
        print('Downloaded {} ...'.format(core))

    # Removes index file for easier extraction
    os.remove('cores/index')


def extract_cores(_location):
    """ Extracts each downloaded core to the RA core directory """
    print('Extracting all cores to: {}'.format(_location))

    for file in os.listdir('cores'):
        archive = zipfile.ZipFile('cores/{}'.format(file))
        archive.extractall(_location)
        print('Extracted {} ...'.format(file))


def clean_up():
    """ Removes all the downloaded files """
    if os.listdir('cores'):
        rmtree('cores/')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--platform', metavar='STRING', required=False,
                        help='Platform you desire to download for')

    parser.add_argument('-a', '--architecture', metavar='STRING', required=False,
                        help='Architecture for tha platform you desire to download for')

    parser.add_argument('-l', '--location', metavar='STRING', required=False,
                        help='Location you wish the cores to extract to')

    parser.add_argument('-k', '--keep', action='store_true',
                        help='Keeps downloaded core archives')

    args = parser.parse_args()
    main(args)
