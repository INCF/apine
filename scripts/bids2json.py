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
#    pip install pybids duecredit
#

from argparse import ArgumentParser
from bids.grabbids import BIDSLayout
from collections import OrderedDict
import os.path as op
import json

# Crawls BIDS dataset and turns it into a JSON
def craftBIDS(bids_dir):
    bids = BIDSLayout(bids_dir)
    bids_dict = OrderedDict()

    desc = op.join(bids_dir, 'dataset_description.json')
    part = op.join(bids_dir, 'participants.tsv')
    sesh = op.join(bids_dir, 'sessions.tsv')
    scan = op.join(bids_dir, 'scans.tsv')
    read = op.join(bids_dir, 'README')
    chng = op.join(bids_dir, 'CHANGES')

    bids_dict['dataset_description'] = json.load(open(desc))
    if op.isfile(part): bids_dict['demographics'] = part
    if op.isfile(sesh): bids_dict['sessions'] = sesh
    if op.isfile(scan): bids_dict['scans'] = scan
    if op.isfile(read): bids_dict['README'] = read
    if op.isfile(chng): bids_dict['CHANGES'] = chng
    
    bids_dict['participants'] = OrderedDict()
    for subid in bids.get_subjects():
        part_dict = OrderedDict()
        #TODO: remove once @zorro patches in grabbids
        if not op.isdir(op.join(bids_dir, 'sub-{}'.format(subid))):
            print("sub-{} detected, but no directory found!!".format(subid))
            continue
        part_dict["sessions"] = OrderedDict()
        nosesh = len(bids.get_sessions()) == 0
        sesh_array = ["1"] if nosesh else bids.get_sessions()
        for sesid in sesh_array:
            sesh_dict = OrderedDict()
            for mod in bids.get_modalities():
                sesh_dict[mod] = OrderedDict()
                if nosesh:
                    data = bids.get(subject=subid, modality=mod, extensions="nii|nii.gz")
                else:
                    data = bids.get(subject=subid, session=sesid, modality=mod, extensions="nii|nii.gz")

                for dat in data:
                    if mod == 'anat':
                        ty = dat.type
                        sesh_dict[mod][ty] = OrderedDict()
                        sesh_dict[mod][ty]["filename"] = dat.filename
                        if bids.get_metadata(dat.filename) is not None:
                            sesh_dict[mod]["metadata"] = bids.get_metadata(dat.filename)
                    elif mod == "dwi":
                        if bids.get_metadata(dat.filename) is not None:
                            sesh_dict[mod]["metadata"] = bids.get_metadata(dat.filename)
                        sesh_dict[mod]["filename"] = dat.filename
                        sesh_dict[mod]["bval"] = bids.get_bval(dat.filename)
                        sesh_dict[mod]["bvec"] = bids.get_bvec(dat.filename)
                    elif mod == "func":
                        task = dat.task
                        sesh_dict[mod][task] = OrderedDict()
                        if bids.get_metadata(dat.filename) is not None:
                            sesh_dict[mod][task]["metadata"] = bids.get_metadata(dat.filename)
                        sesh_dict[mod][task]["metadata"] = bids.get_metadata(dat.filename)
                        sesh_dict[mod][task]["filename"] = dat.filename
                        if bids.get_events(dat.filename) is not None:
                            sesh_dict[mod][task]["events"] = bids.get_events(dat.filename)
                    else:
                        print("modality {} not found?".format(mod))

            part_dict["sessions"][sesid] = sesh_dict
        bids_dict['participants'][subid] = part_dict
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

    bids_data = craftBIDS(bids_dir)
    if out_file is not None:
        myjson = json.dumps(bids_data, indent=4)
        with open(out_file, 'w') as fhandle:
            fhandle.write(myjson)
    else:
        print(json.dumps(bids_data, indent=4))


if __name__ == "__main__":
    main()
