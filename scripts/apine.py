#!/usr/bin/env python
#
# MIT License
# Copyright (c) INCF
#
# apine.py
# Utility for interacting with Apine objects
# Created 10/12/2017 initially by G. Kiar
#
# To install dependencies, in a fresh virtual environment run:
#    pip install jsonschema
#

from argparse import ArgumentParser
from collections import OrderedDict
from copy import deepcopy
import os.path as op
from jsonschema import validate, ValidationError
import json


def validateApineObj(dataset_descriptor, apine=None):
    """validateApineObj takes an Apine dataset descriptor, and validates its
    compliance with the Apine schema (which can be specified from command-line,
    or the default file used).

    Parameters
    ----------
    dataset_descriptor : str
        The path to the dataset Apine object.
    apine : str
        The path to the Apine schema definition, if you wish to use a definition
        other than the default.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        dobj = json.load(open(dataset_descriptor))

        if apine is None:
            apine = op.join(op.dirname(op.realpath(__file__)), '..', 'apine.schema.json')
        aobj = json.load(open(apine))

        for dentry in dobj:
            valid = validate(schema=aobj, instance=dentry)

        print("Apine validation OK!")
        return True
    
    except ValidationError as e:
        print("Validation failed: {}".format(e.message))
        print("Violating entry:")
        print(json.dumps(dentry, indent=4)) 
        return False


def main(args=None):
    parser = ArgumentParser(description="Utility for parsing and validating Apine files")
    parser.add_argument("descriptor", action="store", help="Path to dataset Apine descriptor")
    results = parser.parse_args() if args is None else parser.parse_args(args)

    validateApineObj(results.descriptor)

if __name__ == "__main__":
    main()
