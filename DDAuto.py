#Written by Chelsea Parlett (2016) for the Working Memory and Plasticity lab and
#collaborators. For questions email cparlett@uci.edu

import re, csv,os, os.path
import glob
import shutil
import numpy as np
import pandas as pd
from operator import eq
from scipy.stats.mstats import gmean

# __all__ = ["MakeList", "CheckIdeals", "RunData"]

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def MakeList(dictionary):
    listobj = []
    for i in ks:
        listobj.append(dictionary[i])
    return listobj
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def CheckIdeals(idealList,list1):
    CL = []
    for ideal in idealList:
        geos = []
        x = map(eq,ideal,list1)
        count = float(x.count(True))
        CL.append(count/9)
        maxValue = max(CL)
        for i in range(0,len(CL)):
            if CL[i] == maxValue:
                geos.append(kEst[i])
        else:
            this = gmean(geos)
    if test:
        print "List of Bayes Proportions"
        print CL
        print "Maximum Value"
        print maxValue
        print "GEOS"
        print geos
    return this

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
participantidtype='[0-9][0-9][0-9]'
test = True
ks = [0.25, 0.1, 0.041, 0.016, 0.006, 0.0025, 0.001, 0.0004, 0.00016]
kEst = [0.25, 0.159, 0.065, 0.026, 0.0098, 0.0039, 0.0016, 0.00063, 0.00025, 0.00016]
errorsFixed = 0
bin1IDEAL = [0,0,0,0,0,0,0,0,0]
bin2IDEAL = [1,0,0,0,0,0,0,0,0]
bin3IDEAL = [1,1,0,0,0,0,0,0,0]
bin4IDEAL = [1,1,1,0,0,0,0,0,0]
bin5IDEAL = [1,1,1,1,0,0,0,0,0]
bin6IDEAL = [1,1,1,1,1,0,0,0,0]
bin7IDEAL = [1,1,1,1,1,1,0,0,0]
bin8IDEAL = [1,1,1,1,1,1,1,0,0]
bin9IDEAL = [1,1,1,1,1,1,1,1,0]
bin10IDEAL = [1,1,1,1,1,1,1,1,1]

ideals = [bin1IDEAL,bin2IDEAL,bin3IDEAL,bin4IDEAL,bin5IDEAL,bin6IDEAL,
bin7IDEAL,bin8IDEAL,bin9IDEAL,bin10IDEAL]
#----------------------------------------------------------------------------
pattern = participantidtype + '_20[0-9][0-9]_[A-Z][a-z][a-z]_[0-9][0-9]_[0-9][0-9][0-9][0-9]_[0-9]*.csv'
if os.path.exists('analysis.csv'):
    writer = csv.writer(open('analysis.csv', 'ab'))  # open filewriter
else:
    writer = csv.writer(open('analysis.csv', 'wb'))
    writer.writerow(
        ['Subject', 'Session','Small K', 'Medium K', 'Large K', 'Overall K'])  # write headers
CurrDir = os.getcwd()
print "You're in " + CurrDir
print "__________________"
filenames = glob.glob(pattern)
new = sorted(filenames)#will sort

for f in new: #for file in folder
    subSearch = '(' + participantidtype+ ')' + '_20'
    subject = re.findall(subSearch, f)
    subject = subject[0]
    if test:
        print "filename: " + f
    #define dictionaries to store values
    small = {}
    medium = {}
    large = {}
    smallList = []
    mediumList = []
    largeList = []



    reader = csv.DictReader(open(f, 'rU'))


    for row in reader: #Load Data
        session = row['Session#']
        diffBin = row['DelayedRewardBin']
        k = float(row['k'])
        response = int(row['LargerLater?'])


        if diffBin == 'Small' and k == 0.01:
            k = 0.001 #because old psychpy script coded this one wrong
            print "fixed error"
            errorsFixed += 1
        if diffBin == 'Small' and k == 0.014:
            k = 0.041
            print "fixed error"
            errorsFixed += 1


        if diffBin == 'Small':
            small[k] = small.get(k, response) # {0.25: 1, 0.1: 1}

        elif diffBin == 'Medium':
            medium[k] = medium.get(k, response)# {0.25: 1, 0.1: 1}

        elif diffBin == 'Large':
            large[k] = large.get(k, response)# {0.25: 1, 0.1: 1}

    if test:
        print "DICTIONARIES"
        print "small", small
        print "medium", medium
        print "large",large

    if len(small) <9: #skip incomplete trials
        continue
        print "Incomplete"

    #make lists for comparison with "ideals"
    smallList = MakeList(small) # [1,1,1,1,0,0...n]
    mediumList = MakeList(medium) # [1,1,1,1,0,0...n]
    largeList = MakeList(large) # [1,1,1,1,0,0...n]

    if test:
        print "LISTS"
        print "small", smallList
        print "medium", mediumList
        print "large", largeList


    smallK = CheckIdeals(ideals, smallList) #compare list to each of possible "ideals"
    mediumK = CheckIdeals(ideals, mediumList)
    largeK = CheckIdeals(ideals, largeList)

    writer.writerow([subject, session, smallK, mediumK, largeK, gmean([smallK,mediumK, largeK])])
