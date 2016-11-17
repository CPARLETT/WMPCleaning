from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil


__all__ = ['getFiles', 'checkForOutFile']

def getFiles(pattern = '*.csv'):
    CurrDir = os.getcwd()
    print "You're in " + CurrDir
    print "__________________"
    print "STARTED"
    filenames = glob.glob(pattern)
    return filenames
def checkForOutFile(outputName = 'clean.csv', headers = ['PID', 'Date']):
    if os.path.exists(outputName):
        writer = csv.writer(open(outputName, 'ab'))  # open filewriter
    else:
        writer = csv.writer(open(outputName, 'wb'))
        writer.writerow(headers)  # write headers
    return writer
