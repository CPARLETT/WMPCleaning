from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil

#TODO
#Separate by Session as well?

ColumnOfInterest = 'xx'
test = False
numSplits = 2
i = 1
checkForBadRow = 'x' #what column will be able to tell you to skip a row?
badValue = 'x' #what will the value be if you DO Want ot skip that row?
pid = 'pidIsCalled' #what is the PID column called??

#REGEX to find PID
CurrDir = os.getcwd()
if test:
    print "You're in " + CurrDir

    print "__________________"

    print "STARTED"
filenames = glob.glob('*.csv')
print "FILENAME: ", filenames




#start the file stuff
for name in filenames: #each session
    reader = csv.DictReader(open(name, 'rU'))  # open reader

    outputName1 = "splitForCA1.csv"
    outputNameAll = "splitForCAAll.csv"

    data = {}


    if os.path.exists(outputName1):
        writer1 = csv.writer(open(outputName1, 'ab'))  # open filewriter
    else:
        writer1 = csv.writer(open(outputName1, 'wb'))
        writer1.writerow(['PID', '1', '2'])  # write headers

    if os.path.exists(outputNameAll):
        writerAll = csv.writer(open(outputNameAll, 'ab'))  # open filewriter
    else:
        writerAll = csv.writer(open(outputNameAll, 'wb'))
        writerAll.writerow(reader.fieldnames + ['X'])  # write headers


    for row in reader: #get info from each file
        if row[checkForBadRow] == badValue:
            continue

        Subject = row[pid]
        ValueWeCareAbout = row[ColumnOfInterest] #value that we want

        x = 'na'
        if i%2 == 0:
            x = 1
        else:
            x = 2

        writerAll.writerow(row + [x])

        data[Subject] = data.get(Subject, {})
        data[Subject][x] = data.get(x, [])
        data[Subject][x].append(ValueWeCareAbout) # {101:{1:[], 2:[]}, 102: {1:[], 2:[]}...}

    for key in data:
        writer1.writerow([key, np.mean(data[key][1]), np.mean(data[key][2])])







for sid in ACC:
    for sess in ACC[sid]:
        # ['PID', 'Session', 'RT1', 'RT2', 'RT All','ACC1', 'ACC2', 'ACC All',
        # 'axRT1', 'axRT2', 'axRT All','axACC1', 'axACC2', 'axACC All'])  # write headers
        writer.writerow([sid, sess, np.nanmean(RT[sid][sess]['RT1']), np.nanmean(RT[sid][sess]['RT2']),
        np.nanmean(RT[sid][sess]['RT1']+RT[sid][sess]['RT2']),np.nanmean(ACC[sid][sess]['ACC1']),
        np.nanmean(ACC[sid][sess]['ACC2']),np.nanmean(ACC[sid][sess]['ACC1']+ACC[sid][sess]['ACC2']),

        np.nanmean(RTAX['AX'][sid][sess]['RTAX1']), np.nanmean(RTAX['AX'][sid][sess]['RTAX2']),
        np.nanmean(RTAX['AX'][sid][sess]['RTAX1']+RTAX['AX'][sid][sess]['RTAX2']),np.nanmean(ACCAX['AX'][sid][sess]['ACCAX1']),
        np.nanmean(ACCAX['AX'][sid][sess]['ACCAX2']),np.nanmean(ACCAX['AX'][sid][sess]['ACCAX1']+ACCAX['AX'][sid][sess]['ACCAX2'])
        ])
