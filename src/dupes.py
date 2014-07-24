#!/usr/bin/env python3
"""Find duplicate files

Usage:
  dupes.py [-e GLOB]... [-r REGEX]... [-R REGEX]... [PATH ...]
  dupes.py (-h | --help)
  dupes.py --version

Arguments:
  PATH ...                          Scan the given directories or
                                    current dir if omitted.

Options:
  -e GLOB --exclude=GLOB            Exclude glob pattern from matches.
  -r REGEX --exclude-re=REGEX       Exclude regex pattern from matches.
  -R REGEX --iexclude-re=REGEX      Same but case-insensitive.

  -h --help                         Show this screen.
  --version                         Show version.
"""

__version__ = '1.0.0'

import os
import re
from collections import defaultdict
from fnmatch import fnmatch
from itertools import chain

from docopt import docopt


def exclude_name_factory(exclude_glob=None, exclude_re=None, iexclude_re=None):
    if exclude_glob is None:
        exclude_glob = []

    test_exclude_glob = lambda name: any((
        fnmatch(name, glob) for glob in exclude_glob
    ))

    if exclude_re is None:
        exclude_re = []
    exclude_re = [re.compile(regex) for regex in exclude_re]

    test_exclude_re = lambda name: any((
        regex.search(name) for regex in exclude_re
    ))

    if iexclude_re is None:
        iexclude_re = []
    iexclude_re = [re.compile(regex, re.IGNORECASE) for regex in iexclude_re]

    test_iexclude_re = lambda name: any((
        regex.search(name) for regex in iexclude_re
    ))

    return lambda name: any((
        test_exclude_glob(name), test_exclude_re(name), test_iexclude_re(name)
    ))


def get_duped_filenames(target_dirs, **kwargs):
    seen_names = defaultdict(set)
    test_name_f = exclude_name_factory(**kwargs)

    walk_dirs = (os.walk(target) for target in target_dirs)
    for dirpath, dirnames, filenames in chain.from_iterable(walk_dirs):
        for filename in filenames:
            if not test_name_f(filename):
                seen_names[filename].add(dirpath)

    return dict(
        (filename, dirpaths)
        for filename, dirpaths in seen_names.items()
        if len(dirpaths) > 1
    )


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)

    kwargs = dict(
        exclude_glob=arguments['--exclude'],
        exclude_re=arguments['--exclude-re'],
        iexclude_re=arguments['--iexclude-re'],
    )
    duped_filenames = get_duped_filenames(arguments['PATH'] or ['.'], **kwargs)

    for filename, dirpaths in duped_filenames.items():
        print(filename)
        for dirpath in dirpaths:
            print("\t{}".format(os.path.join(dirpath, filename)))
