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
    obj = {}
    # Give schema and data objects nicer names
    obj["schema"] = apPine.config["schema"]
    obj["dataobjs"] = apPine.config["dataobjs"]

    # Extract valid query strings
    obj["queryvars"] = list(obj["schema"]["properties"].keys())

    # Parse request
    obj["search"] = request.args.get("q")
    obj["query"] = {}
    obj["invalid"] = []

    search_comps = obj["search"].replace(" ", "").split("&")
    for compi in search_comps:
        exp = compi.split("=")
        lhs = exp[0]
        rhs = exp[1] if len(exp) > 1 else "*"

        # If a valid query argument was provided... process it.
        if lhs in obj["queryvars"]:
            obj["query"][lhs] = rhs.split(",")

        # If an invalid argument was provided... ignore it loudly.
        else:
            obj["invalid"] += [lhs]

    # If invalid query params, return without searching
    if len(obj["invalid"]):
        return jsonify(obj)

    # If a valid query, perform search
    obj["summary"] = {}
    # Summarize every collection...
    for dkey in obj["dataobjs"]:
        tmpobj = obj["dataobjs"][dkey]
        tmpsummary = {
                      var: [
                            entry[var]
                            for entry in tmpobj
                            if entry.get(var)
                            if type(entry)
                           ]
                      for var in obj["queryvars"]
                     }
        obj["summary"][dkey] = {
                                k: list(set([i
                                             for it in tmpsummary[k]
                                             for i in it
                                            ]))
                                   if len(tmpsummary[k]) and type(tmpsummary[k][0]) == list
                                   else list(set(tmpsummary[k]))
                                for k in tmpsummary
                               }

    # Now, parse the summaries with 
    print(obj["query"])
    obj["result"] = []
    for dkey in obj["summary"]:
        tmpsummary = obj["summary"][dkey]
        valid = True
        for field in obj["query"]:
            for item in obj["query"][field]:
                if item == "*":
                    print(field, dkey)
                    if not tmpsummary.get(field):
                        valid = False
                        break
                elif item not in tmpsummary[field]:
                    valid = False
                    break
        if valid:
            obj["result"] += [dkey]

    return jsonify(obj)
