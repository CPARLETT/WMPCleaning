from __future__ import division
try:
    import re, csv, os, os.path
    import numpy as np
except:
    print "ERROR: Install numpy  using pip"
try:
    import glob
except:
    print "ERROR: Install glob using pip"
try:
    import shutil
except:
    print "ERROR: Install shutil using pip"

#TODO

def DRM(numBlocks = 6, test = False, Block = True, Level = True, Session = True ):

    CurrDir = os.getcwd()
    print "You're in " + CurrDir
    print "__________________"
    print "STARTED"
    name = 'DRMRecognition.csv'

    reader = csv.DictReader(open(name, 'rU'))  # open reader
    outputName = "DRMclean.csv"

    accuracy = {}
    reactionTime = {}

    if os.path.exists(outputName):
        writer = csv.writer(open(outputName, 'ab'))  # open filewriter
    else:
        writer = csv.writer(open(outputName, 'wb'))
        writer.writerow(
            ['PID', 'Date', 'Session', 'ACC', 'RT'])  # write headers


    for row in reader: #get info from each file
        if 'Word List' not in row['ExperimentName']:
            continue
        pid = row['Subject']
        if pid[0:2] == 'SP' or pid[0:2] == 'sp':
            pid = pid[2:]
        session = row['Session']
        date = row ['SessionDate']
        acc = int(row['WordPresenter.ACC'])
        rt = int(row['WordPresenter.RT'])

        accuracy[pid] = accuracy.get(pid, {})
        accuracy[pid][session] = accuracy[pid].get(session, [])
        accuracy[pid][session].append(acc)

        reactionTime[pid] = reactionTime.get(pid, {})
        reactionTime[pid][session] = reactionTime[pid].get(session, [])
        reactionTime[pid][session].append(rt)

    for pid in accuracy:
        print pid
        for session in accuracy[pid]:
            print session
            writer.writerow([
            pid,
            date,
            session,
            np.mean(accuracy[pid][session]),
            np.mean(reactionTime[pid][session])
            ])



DRM()
