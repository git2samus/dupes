#!/usr/bin/env python3
import os
import sys
from collections import defaultdict
from itertools import chain
from pprint import pprint


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
    args = sys.argv[1:] or tuple('.')
    pprint(get_duped_filenames(args))
