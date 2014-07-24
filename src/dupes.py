#!/usr/bin/env python3
"""Find duplicate files

Usage:
  dupes.py [-i GLOB]... [-m REGEX]... [-M REGEX]...
           [-e GLOB]... [-r REGEX]... [-R REGEX]...
           [PATH ...]
  dupes.py (-h | --help)
  dupes.py --version

Arguments:
  PATH ...                        Scan the given directories or
                                  current dir if omitted.

Options:
  -i GLOB --include=GLOB          Show files matching these glob patterns.
  -m REGEX --include-re=REGEX     Show files matching these regex patterns.
  -M REGEX --iinclude-re=REGEX    Same but case-insensitive.

  -e GLOB --exclude=GLOB          Exclude files matching these glob patterns.
  -r REGEX --exclude-re=REGEX     Exclude files matching these regex patterns.
  -R REGEX --iexclude-re=REGEX    Same but case-insensitive.

  -h --help                       Show this screen.
  --version                       Show version.
"""

__version__ = '1.0.0'

import os
import re
import sys
from collections import defaultdict
from fnmatch import fnmatch
from itertools import chain

from docopt import docopt


def log_stderr(msg):
    sys.stderr.write("{}\n".format(msg))


def test_name_factory(globs, regexs, iregexs):
    regexs = [re.compile(regex) for regex in regexs]
    iregexs = [re.compile(regex, re.IGNORECASE) for regex in iregexs]

    test_globs = lambda name: (
        fnmatch(name, glob) for glob in globs
    )
    test_regexs = lambda name: (
        regex.search(name) for regex in regexs
    )
    test_iregexs = lambda name: (
        regex.search(name) for regex in iregexs
    )

    return lambda name: any(chain(
        test_globs(name), test_regexs(name), test_iregexs(name)
    ))


def iternames(target_dirs, include_patterns, exclude_patterns):
    test_include_name_f = test_name_factory(**include_patterns)
    test_exclude_name_f = test_name_factory(**exclude_patterns)

    if any(include_patterns.values()):
        test_name = lambda name: (
            test_include_name_f(name) and not test_exclude_name_f(name)
        )
    else:
        test_name = lambda name: (
            not test_exclude_name_f(name)
        )

    walk_dirs = (os.walk(target) for target in target_dirs)
    for dirpath, _, filenames in chain.from_iterable(walk_dirs):
        for filename in filenames:
            if test_name(filename):
                yield filename, dirpath


def get_duped_filenames(target_dirs, include_patterns, exclude_patterns):
    seen_names = defaultdict(set)

    filename_gen = iternames(target_dirs, include_patterns, exclude_patterns)
    for filename, dirpath in filename_gen:
        seen_names[filename].add(dirpath)

    return dict(
        (filename, dirpaths)
        for filename, dirpaths in seen_names.items()
        if len(dirpaths) > 1
    )


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)

    target_dirs = []
    for target_dir in arguments['PATH'] or ['.']:
        if os.path.isdir(target_dir):
            target_dirs.append(target_dir)
        else:
            log_stderr(
                "WARNING: Argument '{}' is not a directory.".format(target_dir)
            )

    include_patterns = dict(
        globs=arguments['--include'],
        regexs=arguments['--include-re'],
        iregexs=arguments['--iinclude-re'],
    )

    exclude_patterns = dict(
        globs=arguments['--exclude'],
        regexs=arguments['--exclude-re'],
        iregexs=arguments['--iexclude-re'],
    )

    duped_filenames = get_duped_filenames(
        target_dirs, include_patterns, exclude_patterns
    )

    for filename, dirpaths in duped_filenames.items():
        print(filename)
        for dirpath in dirpaths:
            print("\t{}".format(os.path.join(dirpath, filename)))
