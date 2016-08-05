#! /usr/bin/python
import re
from collections import defaultdict
import argparse

def main(args):

    # the hard-code part
    files = ['access.log']
    words_to_check = ['appid=61']
    result_prefix = 'shrink_'

    # override if parameters given through CLI
    if args.patterns:
        words_to_check = args.patterns

    if args.files:
        files = args.files

    if args.prefix:
        result_prefix = args.prefix

    # start to handle
    for filename in files:
        with open(filename) as f:
            with open(result_prefix + filename, 'w') as sf:
                for line in f.readlines():
                    if all(x in line for x in words_to_check):
                        sf.write(line)

                sf.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--files', nargs='+')
    parser.add_argument('-p','--patterns', nargs='+')
    parser.add_argument('-pr','--prefix')

    args = parser.parse_args()
    main(args)

