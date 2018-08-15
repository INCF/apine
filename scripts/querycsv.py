#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

import os
import os.path as op
import pandas as pd
import json
from collections import OrderedDict
from argparse import ArgumentParser

def toNumber(s):
    try:
        val = float(s)
        return val
    except ValueError:
        return s


def prepareData(csvfile):
    df = pd.read_csv(csvfile)
    return df


def getOptions(dataObj, column=None):
    if column is None:
        columns = dataObj.columns
    else:
        columns = [column]

    options = OrderedDict()
    for column in columns:
        options[column] = list(dataObj[column].unique())
    return options


def queryData(dataObj, query):
    query += ',' if ',' not in query else ''
    cleanQuery = {q.split('=')[0].strip(' '): q.split('=')[1].strip(' ')
                  if len(q.split('=')) > 1 else True
                  for q in query.split(',')
                  if len(q.strip(' ')) > 0}

    resu = dataObj
    for cq in cleanQuery.keys():
        val = toNumber(cleanQuery[cq])
        resu = resu.loc[resu[cq] == val]
    return resu


def main(args=None):
    parser = ArgumentParser('querycsv')
    parser.add_argument("csvfile", action="store", help="the csv file")
    parser.add_argument("--query", "-q", action="store", help="the query")
    result = parser.parse_args() if args is None else parser.parse_args(args)

    csvfile = result.csvfile
    query = result.query
    dataObj = prepareData(csvfile)
    options = getOptions(dataObj)

    if query is None:
        for opt in options:
            print(opt + ":")
            for val in options[opt]:
                print("  - " + str(val))
    else:
        print(queryData(dataObj, query))


if __name__ == "__main__":
    main()
