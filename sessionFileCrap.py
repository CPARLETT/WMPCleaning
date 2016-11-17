from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil

#TODO
#make composite file as well?
folders = glob.glob('[0-9][0-9][0-9]')
f2 = glob.glob('SP[0-9][0-9][0-9]')
folders = folders + f2
test = False
CurrDir = os.getcwd()

print "Folders: ", folders

for folder in folders:
    log = False
    os.chdir(CurrDir + "\\" + folder)
    print "You're in  ", os.getcwd()
    filenames = glob.glob('*.session')
    if len(filenames) <1:
        filenames = glob.glob('*.log')
        log = True

    for filename in filenames:
        with open(filename, 'U') as f:
          a = f.readlines()
        print filename
        if log:
            print a
        outputFileName = re.sub('\.session', '.csv', filename)
        if log:
            outputFileName = re.sub('\.log', '.csv', filename)
        if os.path.exists('clean'):
            print "clean exists"
        else:
            os.makedirs('clean')
        outputFileName = 'clean\\' + outputFileName
        text_file = open(outputFileName, "w")


        pid = re.findall('([0-9a-zA-Z]+)-session[0-9]', filename)[0]
        if pid[0:2] == 'SP':
            pid = pid[2:]
        if test:
            print pid
        date = re.findall('-(20[0-9][0-9]-[0-9][0-9]-[0-9][0-9])-[0-9][0-9]-[0-9][0-9]', filename)[0]
        time = re.findall('-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-([0-9][0-9]-[0-9][0-9])', filename)[0]
        time = re.sub('-', ':', time)
        if test:
            print date
            print time

        b = []
        dontStartYet = False
        for x in a:
            if 'SessionNumber'in x:
                dontStartYet = True
            if dontStartYet:

                x = re.sub('\\n', '', x)
                x = re.sub('%', '', x)
                x = x.rstrip().lstrip()
                x = re.sub(' ', ',', x)
                if 'Session,Log' in x or 'debug,seed:' in x or 'Intended,Stage' in x or 'Timestamp' in x or '{' in x:
                    continue
                if 'SessionNumber' in x:
                    x = 'PID,Date,Time,' + x
                    b.append(x)
                elif x != '':
                    b.append(pid + ','  + date + ',' + time + ',' + x)

        for thing in b:
            text_file.write(thing + '\n')
        text_file.close()
os.chdir(CurrDir)
