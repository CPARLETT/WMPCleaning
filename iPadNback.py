from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil

#TODO
#delete csv files when Done


# refdic = {} # {pid: condition}
# reference = csv.DictReader(open('conditions.csv', 'rb'))
# for r in reference: #get reference of conditions
#     c = r['Condition'] #condition of participant
#     p = r['SID'] #pid
#     refdic[p]= refdic.get(p,c) #add to refdic so I have a dict of participant ids:condition


#REGEX to find PID
CurrDir = os.getcwd()
print "You're in " + CurrDir
print "__________________"
print "STARTED"
test = True

folders = glob.glob('[0-9][0-9][0-9]') + glob.glob('SP[0-9][0-9][0-9]')
for folder in folders:
    try:
        os.chdir(CurrDir + "\\" + folder + '\\' + 'clean')
    except:
        print "No clean folder for ", folder
        continue
    filenames = glob.glob('*.csv')


    NbackCol = 'N-Back'

    for name in filenames: #each session
        if 'session' not in name:
            continue
        reader = csv.DictReader(open(name, 'rU'))  # open reader
        outputName = CurrDir + '\\' +"clean.csv"
        hits = []
        fa = []
        levels = []

        if os.path.exists(outputName):
            writer = csv.writer(open(outputName, 'ab'))  # open filewriter
        else:
            writer = csv.writer(open(outputName, 'wb'))
            writer.writerow(
                ['PID', 'Date', 'Session', 'PR', 'Average N'])  # write headers


        for row in reader: #get info from each file
            pid = row['PID']
            date = row['Date']
            session = row['SessionNumber']
            if len(row) <5:
                print "short row or level 1"
                continue
            h = int(row['TP'])
            f = int(row['FP'])
            nback = int(row['N-Back'])
            hits.append(h)
            fa.append(f)
            levels.append(nback)

        if test:
            print name
        writer.writerow([pid, date, session, sum(hits) - sum(fa), np.mean(levels)])
