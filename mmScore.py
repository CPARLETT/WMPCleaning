import re, csv,os, os.path
import glob
from collections import deque


def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow

name = 'Scores.csv'
filenames = glob.glob('*_score.csv')
for f in filenames:
    pid = ''
    session = ''
    score = ''
    print f#for checking purposes, prints file it's processing into terminal
    # reader = csv.reader(open(f, 'rb'))
    if os.path.exists(name):
        writer = csv.writer(open( name ,'ab'))
    else:
        writer = csv.writer(open( name ,'wb'))
        writer.writerow(['pid','session', 'version','score'])
    lastRow = get_last_row(f)
    pid = lastRow[0]
    session = lastRow[1]
    score = lastRow[5]
    reader = csv.reader(open(f, 'rb'))
    row1 = next(reader)
    if row1[3] == 'twist':
        version = "B"
    else if row1[3] == "apple":
        version = "A"
    else:
        version = "problem"
    writer.writerow([pid,session, version, score])
