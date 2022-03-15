#! /usr/bin/env python3

import argparse
import atexit
import collections
import os
import re
import sys

from xopen import xopen

from pathlib import Path
from xopen import xopen
from pprint import pprint


"""
TODO:
    - add filtering so that the number of candidate files is low
    - loads seqs
    - output hierarchy - batch / file; or maybe just batch files to  keep it
    simple and then some piping ot minimap in another script?
       - maybe read name - list of refs?
    - double check that reads are in the right order
    - references don't have to be - we will be just iterating through them and
    side checking dict queries
    - document the assumption that the number of reads is small
"""



KEEP = 100
"""
For every read we want to know top 100 matches

Approach:
    - for every read keep a buffer in memory
    - iterate over all translated cobs outputs
    - keep just top k scores
"""




def cobs_iterator(cobs_matches_fn):
    """Iterator for cobs matches.

    Assumes that cobs ref names start with a random sorting prefix followed by
    an underscore.

    Args:
        cobs_matches_fn (str): File name of cobs output.

    Returns:
        matches (list): List of assignments of the same read, in the form (ref, qname, kmers)



    Todo:
        - if necessary in the future, add batch name from the file name
    """
    qname = None
    matches_buffer=[]
    print(f"Translating matches {cobs_matches_fn}", file=sys.stderr)
    with xopen(cobs_matches_fn) as f:
        for x in f:
            x = x.strip()
            if not x:
                continue
            if x[0] == "*":
                ## HEADER
                # empty buffer
                if qname is not None:
                    yield matches
                    matches_buffer=[]
                # parse header
                parts = x[1:].split()
                qname = part[0].split(" ")[0] # remove fasta comments
                nmatches = int(parts[2])
            else:
                ## MATCH
                tmp_name, kmers = x.split()
                rid, ref = tmp_name.split("_")
                matches_buffer.append( (ref, qname, kmers) )
    yield matches_buffer



class SingleQuery:
    """A simple optimized buffer for keeping top matches for a single read accross batches.

    Args:
        keep_matches (int): The number of top matches to keep.


    Attributes:
        _matches (list): A list of (ref, kmers)
    """

    def __init__(self, keep_matches=100):
        self._min_matching_kmers = 0  #should be increased once the number of records >keep
        self._matches=[]
        self._qname=None # will be assigned automatically and checked automatically

    def add_matches(self, matches):
        """Add matches.
        """
        for mtch in matches:
            ref, qname, kmers=mtch
            assert self._qname is None or self._qname==qname
            self._qname = qname
            if kmers >= self._min_matching_kmers:
                self._matches.append( (ref, kmers) )

    def _housekeeping(self):
        ###
        ### TODO: Finish
        ###

        #1. sort
        self._matches.sort(key=lambda x: (x[1], x[0]))
        #2. identify where to stop
        #3. trim the list below
        #4. update _min_kmers_filter according to this value


##
## TODO: add support for empty matches / NA values
##

def merge_and_filter(fns, keep):
    bm = BestMatches(keep)
    for fn in fns:
        bm.process_file(fn)
    bm.print_output()


def main():

    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'match_fn',
        metavar='',
        nargs='+',
        help='',
    )

    parser.add_argument(
        '-k',
        metavar='int',
        dest='keep',
        default=KEEP,
        help=f'no. of best hits to keep [{KEEP}]',
    )

    args = parser.parse_args()
    merge_and_filter(args.match_fn, args.keep)


if __name__ == "__main__":
    main()

