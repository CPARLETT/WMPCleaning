from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil


refdic = {} # {pid: condition}
reference = csv.DictReader(open('conditions.csv', 'rb'))
for r in reference: #get reference of conditions
    c = r['Condition'] #condition of participant
    p = r['SID'] #pid
    refdic[p]= refdic.get(p,c) #add to refdic so I have a dict of participant ids:condition





#REGEX to find PID
CurrDir = os.getcwd()
print "You're in " + CurrDir

print "__________________"

print "STARTED"
filenames = glob.glob('[0-9][0-9][0-9]---*.csv')
print filenames
for name in filenames: #each session
    reader = csv.DictReader(open(name, 'rU'))  # open reader
    pid = re.findall('([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9])---', name)  # find PID
    date = re.findall('---([a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+)---', name)
    print date
    if len(pid) < 1:
        break
    outputName = "clean.csv"
    accuracy2 = {'o': [], 'c': []}
    hits = []
    rtAll = []

    if os.path.exists(outputName):
        writer = csv.writer(open(outputName, 'ab'))  # open filewriter
    else:
        writer = csv.writer(open(outputName, 'wb'))
        writer.writerow(
            ['PID', 'Date', 'EoO', 'EoC', 'Total Errors', 'Hit Rate', 'False ALarm Rate', "Condition", "Group", 'RT'])  # write headers


    for row in reader: #get info from each file
        if len(row) <5 or row["Game Name"] != 'N-Back Baseline' or row['Level'] == '1':
            print "short row or level 1"
            continue
        try:
            rt = int(row['RT'])
            rtAll.append(rt)
        except:
            continue
        rnd = row["Round"]
        if row['ACC'] =='0':
            if row["Participant response"] == 'no tap':
                x = 'o'
                accuracy2[x].append(1)
            elif row['Participant response'] == "tapped screen":
                x = 'c'
                accuracy2[x].append(1)
            else:
                continue
        elif row['ACC'] == '1':
            if row['Participant response'] == 'tapped screen':
                hits.append(1)
    print accuracy2
    eoo = sum(accuracy2['o'])
    eoc = sum(accuracy2['c'])
    rtav = np.mean(rtAll)
    try:
        con = int(refdic[pid[0]])
        if con < 3:
            group = 'MQ'
        else:
            group = 'KB'
    except:
        con = 'QUIT'
        group = 'unkown'
    writer.writerow([pid[0], date[0], eoo , eoc , eoo+eoc, ((30-eoo)/30) ,(eoc/96), con, group, rtav])
