#!/usr/bin/env python

from argparse import ArgumentParser
from os.path import join as opj
from jsonschema import validate, ValidationError
from jsonschema import Draft3Validator, Draft4Validator, SchemaError
import connexion
import fnmatch
import json
import sys
import os

from apine.server import apPine


class ApineError(Exception):
    pass


def getJSON(filename, **kwargs):
    try:
        with open(filename, 'r') as fhandle:
            filedata = json.load(fhandle)

        # If the file is a schema, validate it first with Draf4 and then Draft3
        if kwargs.get("schema"):
            try:
                Draft4Validator.check_schema(filedata)
            except SchemaError as e:
                try:
                    Draft3Validator.check_schema(filedata)
                except SchemaError as er:
                    raise ApineError("\"{0}\" failed JSON Schema validation.\n"
                                     "Draft3 Error: {1}\n\n"
                                     "Draft4 Error: {2}".format(filename,
                                                                str(er),
                                                                str(e)))
        return filedata
    except json.decoder.JSONDecodeError as e:
        raise ApineError("\"{0}\" is not a valid JSON file".format(filename))


def getData(dirname, **kwargs):
    datadict = {}
    for root, directories, filenames in os.walk(dirname):
        for filename in fnmatch.filter(filenames, "*.json"):
            try:
                fname = opj(root, filename)
                tmpdata = getJSON(fname)

                # If a schema is provided, validate object against it...
                schema = kwargs.get("schema")
                if schema:
                    try:
                        # Assumption: the files contain a list of schema objs
                        for obj in tmpdata:
                            validate(obj, kwargs.get("schema"))
                        datadict[fname] = tmpdata

                    except ValidationError as e:
                        if kwargs.get("verbose"):
                            print("Skipping JSON file not complying to schema:"
                                  " {0}".format(fname))

                # ... otherwise, just add it to the stack.
                else:
                    datadict[fname] = tmpdata

            except ApineError as e:
                if kwargs.get("verbose"):
                    print("Skipping invalid JSON file: \"{0}\".".format(fname))

    return datadict


def startServer(schema, dataobjs, **kwargs):
    apPine.config["schema"] = schema
    apPine.config["dataobjs"] = dataobjs

    apPine.run(host=kwargs.get("host") or "0.0.0.0",
               port=kwargs.get("port") or 8080,
               debug=kwargs.get("debug"))


def main():
    parser = ArgumentParser("Apine: querying neurostuff")
    parser.add_argument("schema", action="store", help="Path to valid JSON "
                        "schema summarizing the datasets you wish to query.")
    parser.add_argument("datadir", action="store", help="Basepath of the JSON "
                        "objects complying to the above schema. This path "
                        "will be walked recursively, so ensure your datadir "
                        "is well bounded to obtain reasonable performance.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Toggle"
                        " verbose output messages.")
    parser.add_argument("--port", "-p", action="store", default=8080, type=int,
                        help="Port to route the Apine webserver through. "
                        "Defaults to 8080.")
    parser.add_argument("--debug", "-x", action="store_true", help="Toggle"
                        " development mode.")
    results = parser.parse_args()

    # Convert inputs to dictionary for easy function passing
    schema = results.schema
    datadir = results.datadir

    kwargs = dict(**vars(results))
    del kwargs["schema"]
    del kwargs["datadir"]

    # Load schema and data objects
    if kwargs.get("verbose"):
        print("Locating and validating JSON schema...")
    schema = getJSON(schema, schema=True, **kwargs)

    if kwargs.get("verbose"):
        print("Locating and validating JSON data objects "
              "(this may take some time)...")
    dataobjs = getData(datadir, schema=schema, **kwargs)

    # Once objects and schema are loaded, launch the app
    if kwargs.get("verbose"):
        print("Launching Apine server on port {0}".format(kwargs.get("port")))

    startServer(schema, dataobjs, **kwargs)


if __name__ == '__main__':
    main()
