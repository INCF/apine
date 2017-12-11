#!/usr/bin/env python
#
# MIT License
# Copyright (c) INCF
#
# bids2apine.py
# Utility for converting BIDS datasets to Apine JSON descriptors
# Created 10/12/2017 initially by G. Kiar
#
# To install dependencies, in a fresh virtual environment run:
#    pip install pybids duecredit
#

from argparse import ArgumentParser
from bids.grabbids import BIDSLayout
from collections import OrderedDict
from copy import deepcopy
import os.path as op
import json

# Crawls BIDS dataset and turns it into an Apine JSON object
def generateApine(bids_dir, dset=None):
    """generateApine takes a bids directory and optionally dataset name,
    and generates an Apine JSON object.

    Parameters
    ----------
    bids_dir : str
        The BIDS data directory.
    dset : str
        The dataset name. If none is provided, the directory will be used.

    Returns
    -------
    dict
        Apine dictionary object.
    """
    bids = BIDSLayout(bids_dir)
    apine = list()

    # For every entity...
    for subid in bids.get_subjects():
        current = OrderedDict()
        current["dataset"] = bids_dir if dset is None else dset
        current["participant"] = subid

        if not op.isdir(op.join(bids_dir, 'sub-{}'.format(subid))):
            print("sub-{} detected, but no directory found!!".format(subid))
            continue

        # And for every session...
        nosesh = len(bids.get_sessions()) == 0
        sesh_array = [None] if nosesh else bids.get_sessions()
        for sesid in sesh_array:
            if not nosesh:
                current["session"] = sesid

            # And for every modality...
            for mod in bids.get_modalities():
                current["modality"] = mod

                # Get corresponding data
                if nosesh:
                    data = bids.get(subject=subid, modality=mod, extensions="nii|nii.gz")
                else:
                    data = bids.get(subject=subid, session=sesid, modality=mod, extensions="nii|nii.gz")

                # Now, for every piece of data for this participant, session, and modality...
                for dat in data:
                    # Add the filename
                    current["filename"] = op.basename(dat.filename)
                    cleanname = op.basename(dat.filename).split('.')[0]
                    current["filename_keys"] = [keyval
                                                for keyval in cleanname.split("_")
                                                if "sub-" not in keyval and "ses-" not in keyval]
                    tmp = deepcopy(current) 
                    apine += [tmp]

    return apine


def main(args=None):
    parser = ArgumentParser("BIDS to JSON converter (leveraging pyBIDS)")
    parser.add_argument("bids_dir", action="store",
                        help="The BIDS Directory to be described")
    parser.add_argument("--out_file", "-o", action="store",
                        default=None, help="The resulting JSON file")
    parser.add_argument("--dataset", "-d", action="store",
                        default=None, help="The name of the dataset")
    results = parser.parse_args() if args is None else parser.parse_args(args)

    bids_dir = results.bids_dir
    out_file = results.out_file
    dset = results.dataset

    apine = generateApine(bids_dir, dset=dset)
    if out_file is not None:
        myjson = json.dumps(apine, indent=4)
        with open(out_file, 'w') as fhandle:
            fhandle.write(myjson)
    else:
        print(json.dumps(apine, indent=4))


if __name__ == "__main__":
    main()
