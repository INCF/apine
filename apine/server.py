#!/usr/bin/env python
#
# This software is distributed with the MIT license:
# https://github.com/gkiar/clowdr/blob/master/LICENSE
#
# clowdr/share/server.py
# Created by Greg Kiar on 2018-03-01.
# Email: gkiar@mcin.ca

from flask import Flask, render_template, request, jsonify
import os.path as op
import datetime
import tempfile
import json
import sys
import re
import os


apPine = Flask(__name__, static_url_path='/static')

@apPine.route("/")
def index():
    return apPine.send_static_file("index.html")


@apPine.route("/results")
def parseQuery():
    # Give schema and data objects nicer names
    schema = apPine.config["schema"]
    dataobjs = apPine.config["dataobjs"]
    print(dataobjs.keys())

    # Extract valid query strings
    queryvars = schema["properties"].keys()
    print(queryvars)

    # Parse request
    req = dict(request.args)
    print(req)
    query = []
    invalid = []
    for reqkey in req.keys():
        # If a valid query argument was provided... process it.
        if reqkey in queryvars:
            print(reqkey + "found!")
        # If an invalid argument was provided... ignore it loudly.
        else:
            print("cannot parse" + reqkey)
            invalid += [reqkey]

    # If the query had invalid args, return without searching
    if len(invalid) > 0:
        datadict = {
                        "invalid": list(invalid),
                        "queryvars": list(queryvars),
                        "query": req
                   }
        return jsonify(datadict)

    # If a valid query, perform search
    for dkey in dataobjs.keys():
        dobj = dataobjs[dkey]


    return jsonify(dataobjs)
