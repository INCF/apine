#!/usr/bin/env python
#
# MIT License
# Copyright (c) INCF
#
# bids2json.py
# Utility for converting BIDS datasets to JSON descriptors
# Created 29/08/2017 initially by G. Kiar
#
# To install dependencies, in a fresh virtual environment run:
#    pip install pybids duecredit pandas orderedDict
#

from argparse import ArgumentParser
from bids.grabbids import BIDSLayout
from collections import OrderedDict
import pandas
import json

# Turns BIDS dataset into JSON dictionary
def crawlBIDS(bids_dir, metadata=None, outfile=None):
    # Load BIDS directory as a data framei & initialize dict
    bids_df = BIDSLayout(bids_dir).as_data_frame()
    bids_dict = OrderedDict(metadata)

    task_dict = {}
    # Iterate for each object in the dataset
    for idx in range(len(bids_df)):
        entry = bids_df.iloc[idx]

        # Our action depends on the type of entry we're looking at
        typ = entry.type
        if typ == 'events':
            print(entry)
            #task_dict
            pass
        elif typ == 'description':
            bids_dict['description'] = json.load(open(entry.path, 'r'))
            #print(typ + 'description')
        elif typ == 'dwi':
            pass
            #print(typ + 'dwi')
        elif typ == 'bold':
            pass
            #print(typ + 'bold')
        elif typ == 'T1w':
            pass
            #print(typ + 'T1w')
        else:
            if str(entry.bval) != 'nan' and entry.bval.endswith('.bval'):
                pass
                #print(entry.bval)
            elif str(entry.bvec) != 'nan' and entry.bvec.endswith('.bvec'):
                pass
                #print(entry.bvec)
    return bids_dict

def main(args=None):
    parser = ArgumentParser("BIDS to JSON converter (leveraging pyBIDS)")
    parser.add_argument("bids_dir", action="store",
                        help="The BIDS Directory to be described")
    parser.add_argument("--metadata", "-m", action="store",
                        default=None, help="BIDS Dataset metadata. Must be \
                        formatted as a list of key:value pairs separated by \
                        comma. i.e. name:DS004,url:http://google.com, ...")
    parser.add_argument("--out_file", "-o", action="store",
                        default=None, help="The resulting JSON file")
    results = parser.parse_args() if args is None else parser.parse_args(args)

    bids_dir = results.bids_dir
    out_file = results.out_file

    if results.metadata is not None:
        try:
            metadata = {item.split(':')[0]: item.split(':')[1]
                        for item in results.metadata.split(',')}
        except AttributeError:
            raise(AttributeError, 'malformed metadata string.')
    else:
        metadata = None

    bids_data = crawlBIDS(bids_dir, metadata)
    if out_file is not None:
        json.dump(bids_data, open(out_file, 'w'))
    else:
        print(bids_data)


if __name__ == "__main__":
    main()
