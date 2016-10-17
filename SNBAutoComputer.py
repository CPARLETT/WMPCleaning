#Written by Chelsea Parlett (2016) for the Working Memory and Plasticity lab and
#collaborators. For questions email cparlett@uci.edu
#TODO 10/17/16
#

import re, csv,os, os.path
import glob
import shutil
import numpy as np
import pandas as pd
from operator import eq
from scipy.stats.mstats import gmean

#Params==================================
test = False #print out and create csv with iterations for checking
KeepEmptyRows = False #delete rows with no nback information
rawFile = 'New.csv' #raw datafile name
codeTargetsAs = 'O' #What should targets be coded as, lure type wise? usually O or 0
#Params==================================
csvNbackColName = 'nbacklevel' #What column is n-back level info in?
#Params==================================

def LoadData(filename = rawFile):
    ALL = []
    data = {}
    reader = csv.DictReader(open(filename, 'rU')) #open DictReader
    colNames = reader.fieldnames + ['Nback'] + ['Lure Type'] #add our 2 new cols
    if os.path.exists('output.csv'):
        writer = csv.DictWriter(open('output.csv', 'ab'), colNames)  # open filewriter
        if test:
            print "already here"
    else:
        writer = csv.DictWriter(open('output.csv', 'wb'),colNames)
        writer.writeheader()
        if test:
            print "headerWritten"
    if test:
        print "colnames", colNames
    for row in reader: #create list of rows as Dicts
        ALL.append(row)
    return ALL, writer #data, writer-object

def Block(data, writer):
    if test:
        ForMySakeWriter = csv.writer(open('omgitWorks.csv', 'ab'))
    block = {}
    for i in range(0, len(data)): #for each row
        item = data[i]
        z = 1 # how many back
        howManyBack = 0
        if item['vis_cr'] == '': #write empty information rows still...I guess.
            if KeepEmptyRows:
                writer.writerow(item)
                if test:
                    print "row written"
            else:
                continue
        else: # do the nonEmpty Rows meow
            noMatch = True
            subject = item['Subject']
            session = item['Session']
            nbackLevel = int(item[csvNbackColName])
            block = item['Block']
            stim = item['Stim Location']
            #first, do the checking
            while subject == data[i-z]['Subject'] and session == data[i-z]['Session'] and block == data[i-z]['Block'] and noMatch: #while the previous rows match
                y = "Comparing " + stim +" and " + data[i-z]['Stim Location'] + " which is " + str(z) + " back"
                if test:
                    ForMySakeWriter.writerow([y])
                if stim == data[i-z]['Stim Location']: #if it's the same as x previous
                    if test:
                        ForMySakeWriter.writerow(['It Matched!!!'])
                    noMatch = False


                    #now that we've found the match, write the row!
                    item2 = item
                    item2['Nback'] = z

                    if z == nbackLevel:
                        lt = 'N'
                    elif z < nbackLevel:
                        smallerby = nbackLevel - z
                        lt = "N-" + str(smallerby)
                    elif z > nbackLevel:
                        biggerby = z-nbackLevel
                        lt = "N+" + str(biggerby)


                    item2['Lure Type'] = lt
                    writer.writerow(item2)

                else:
                    z += 1
                    if test:
                        ForMySakeWriter.writerow(['This is Clearly not a Match'])
            if noMatch:
                if test:
                    ForMySakeWriter.writerow(['NoMatch Found'])
                item2 = item
                item2['Nback'] = 0
                item2['Lure Type'] = codeTargetsAs
                writer.writerow(item2)









#Run this stuff
thisList, writer = LoadData()
Block(thisList,writer)

#for testing purposes
if test:
    print "test entry:   ", thisList[0]
