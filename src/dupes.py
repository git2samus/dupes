#!/usr/bin/env python3
"""Find duplicate files

Usage:
  dupes.py [PATH ...]
  dupes.py (-h | --help)
  dupes.py --version

Arguments:
  PATH          Scan the given directories or current dir if ommitted.

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__version__ = '1.0.0'

import os
from collections import defaultdict
from itertools import chain
from pprint import pprint

from docopt import docopt


def get_duped_filenames(target_dirs):
    seen_names = defaultdict(set)

    walk_dirs = (os.walk(target) for target in target_dirs)
    for dirpath, dirnames, filenames in chain.from_iterable(walk_dirs):
        for filename in filenames:
            seen_names[filename].add(dirpath)

    return dict(
        (filename, dirpaths)
        for filename, dirpaths in seen_names.items()
        if len(dirpaths) > 1
    )


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    pprint(get_duped_filenames(arguments['PATH'] or ['.']))
