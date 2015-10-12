#!/usr/bin/python

import pickle
from collections import defaultdict
from collections import OrderedDict
import sys

def recursivePrint(inputData,extraTuple = ()):
    if type(inputData) == dict or type(inputData) == defaultdict \
            or type(inputData) == OrderedDict:
        for extraInfo,data in inputData.iteritems():
            recursivePrint(data,(extraInfo,)+extraTuple)
    elif type(inputData) == list:
        for data in inputData:
            recursivePrint(data,extraTuple)
    else:
        print " ".join([str(x) for x in extraTuple]),inputData
def pickleViewer(inputFile):
    inputData = pickle.load(open(inputFile,'r'))
    print "Viewing pickle file {0} which contains data of type {1}".format(inputFile,type(inputData))
    recursivePrint(inputData)

if __name__ =="__main__":
    assert len(sys.argv) == 2, "Usage: pickleViewer <input.pkl>"
    pickleViewer(sys.argv[1])

