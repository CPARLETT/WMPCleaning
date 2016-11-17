from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil



numBlocks = 6
test = False
#REGEX to find PID
CurrDir = os.getcwd()
print "You're in " + CurrDir

print "__________________"

print "STARTED"
filenames = glob.glob('*[0-9][0-9][0-9]_20[0-9][0-9]_*.csv')
print filenames
if test:
    print "FILENAME: ", filenames
for name in filenames: #each session
    reader = csv.DictReader(open(name, 'rU'))  # open reader
    date = re.findall('(20[0-9][0-9]_[A-Z][a-z][a-z]_[0-9][0-9])', name)

    if test:
        print "DATE: ",date

    outputName = "mathFinal.csv"
    acc = {'Two':[], 'Three': [], "Subtract":[], 'Add': [], 'All': []}
    rt = {'Two':[], 'Three': [], "Subtract":[], 'Add': [],  'All': []}


    if os.path.exists(outputName):
        writer = csv.writer(open(outputName, 'ab'))  # open filewriter
    else:
        writer = csv.writer(open(outputName, 'wb'))
        writer.writerow(
            ['PID', 'Date', 'Session', 'RT TWO', 'RT THREE', 'RT Add','RT Sub', 'RT All', 'ACC TWO', 'ACC THREE', 'ACC Add','ACC Sub', 'Acc All'])  # write headers

    for row in reader: #get info from each file
        try:
            pid = row['Subject#']
            if pid[0:2] == 'SP':
                pid = pid[2:]
            session = row['Session#']
            operation = row['operation']
            operands = row['#operands']
        except:
            continue
        accs = int(row['Correct?'])
        rts = float(row['RT'])
        acc['All'].append(accs)
        rt['All'].append(rts)
        if operation == 'Add':
            acc['Add'].append(accs)
            rt['Add'].append(rts)
        else:
            acc['Subtract'].append(accs)
            rt['Subtract'].append(rts)
        if operands == 'Two':
            acc['Two'].append(accs)
            rt['Two'].append(rts)
        else:
            acc['Three'].append(accs)
            rt['Three'].append(rts)

    writer.writerow([pid, date[0], session,

    np.nanmean(rt['Two']),np.nanmean(rt['Three']),np.nanmean(rt['Add']),np.nanmean(rt['Subtract']),

    np.nanmean(rt['All']),

    np.nanmean(acc['Two']),np.nanmean(acc['Three']),np.nanmean(acc['Add']),np.nanmean(acc['Subtract']),

    np.nanmean(acc['All'])
    ])
