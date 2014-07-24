dupes
=====

Commandline tool to find duplicate files

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
