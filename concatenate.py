from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil

#TODO
#Separate by Session as well?

#REGEX to find PID
CurrDir = os.getcwd()
if test:
    print "You're in " + CurrDir

    print "__________________"

    print "STARTED"
filenames = glob.glob('*.csv')





#start the file stuff
for name in filenames: #each session
    reader = csv.DictReader(open(name, 'rU'))  # open reader

    outputName1 = "concatenated.csv"

    if os.path.exists(outputName1):
        writer1 = csv.writer(open(outputName1, 'ab'))  # open filewriter
    else:
        writer1 = csv.writer(open(outputName1, 'wb'))
        writer1.writerow(reader.fieldnames)  # write headers

    for row in reader: #get info from each file
        writer1.writerow(row)
