import re, csv,os, os.path
import glob

name = 'NewHorizonScores.csv'
filenames = glob.glob('*.csv')
for f in filenames:
    pid = ''
    pacc = []
    print f#for checking purposes, prints file it's processing into terminal
    reader = csv.reader(open(f, 'rb'))
    if os.path.exists(name):
        writer = csv.writer(open( name ,'ab'))
    else:
        writer = csv.writer(open( name ,'wb'))
        writer.writerow(['pid','score'])

    for row in reader:
        if row[0] == 'task' or row[7] == '-':
            continue
        if len(row)<5:
            continue
        pid = int(row[2])
        acc = int(row[7])
        pacc.append(acc)
    s = sum(pacc)
    writer.writerow([pid,s])
